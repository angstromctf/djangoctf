from django.conf import settings
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import viewsets, permissions, status as _status, schemas
from rest_framework.decorators import detail_route, list_route, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework_swagger.renderers import OpenAPIRenderer

from api import serializers, models
from api.permissions import ContestStarted, ContestEnded, HasTeam, not_permission
from api.utils import create_code, create_shell_username, create_shell_password

import hashlib
import logging
import random

logger = logging.getLogger(__name__)
generator = schemas.SchemaGenerator()


@api_view(exclude_from_schema=True)
@renderer_classes([OpenAPIRenderer])
def schema(request):
    return Response(generator.get_schema())


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ContestStarted,)
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer

    @detail_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(ContestEnded),
                                                        HasTeam), serializer_class=serializers.ProblemSubmitSerializer)
    def submit(self, request, pk=None):
        """Handles submissions for specific problems and returns success status."""

        problem = self.get_object()
        team = request.user.profile.team
        guess = request.data['guess'].strip().lower()

        # We've now solved the problem because the solution was correct
        if hashlib.sha512(guess.encode()).hexdigest() == problem.flag:
            if problem not in team.solved.all():
                team.solved.add(problem)

                # Update the team's score
                team.score += problem.value

                # If this problem is supposed to update the team's last submitted time, do that (this is almost always true)
                if problem.update_time:
                    team.score_lastupdate = timezone.now()

                team.save()

                # Add a new CorrectSubmission object corresponding to having solved the problem
                solution = models.CorrectSubmission(team=team, problem=problem, new_score=team.score)
                solution.save()

            return Response({})

        # The submission was incorrect
        else:
            if models.IncorrectSubmission.objects.filter(team=team, problem=problem, guess=guess).exists():
                # This is a new incorrect flag
                solution = models.IncorrectSubmission(team=team, problem=problem, guess=guess)
                solution.save()

            return Response({}, status=_status.HTTP_406_NOT_ACCEPTABLE)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(HasTeam)),
                serializer_class=serializers.TeamCreateSerializer)
    def new(self, request):
        """Creates new teams for the competition."""

        # Check if this team already exists
        if models.Team.objects.filter(name=request.data['name']).exists():
            return Response({}, _status.HTTP_409_CONFLICT)

        code = create_code()
        shell_username = create_shell_username()
        shell_password = create_shell_password()

        # Check if we need to set up a shell account for the team
        if settings.SHELL['enabled']:
            import paramiko

            # SSH to shell server
            private_key = paramiko.RSAKey.from_private_key_file(settings.SHELL['ssh_key_path'])
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=settings.SHELL['hostname'], username='root', pkey=private_key)

            # Create the account
            stdin, stdout, stderr = ssh.exec_command("addctfuser " + shell_username + " " + shell_password)

            stdout_data = stdout.read().decode('utf-8')
            stderr_data = stderr.read().decode('utf-8')

            # Log if something went wrong
            if not stderr:
                logger.error(
                    "Error while creating shell account.\nstdout: {}\nstderr: {}".format(stdout_data, stderr_data))

        # Create the team
        team = models.Team(name=request.data['name'],
                           school=request.data['school'],
                           shell_username=shell_username,
                           shell_password=shell_password,
                           code=code,
                           eligible=request.user.profile.eligible)
        team.save()

        # Add the user to that team
        request.user.profile.team = team
        request.user.profile.save()

        return self.account(request)

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(HasTeam)),
                serializer_class=serializers.TeamJoinSerializer)
    def join(self, request):
        """Adds the user to a pre-existing team."""

        team = get_object_or_404(models.Team, code=request.data['code'])

        if team.members.count() < settings.USERS_PER_TEAM:
            # Compute the team's eligibility by combining its current eligibility with the user's eligibility
            team.eligible = team.eligible and request.user.profile.eligible
            team.save()

            # Add the user to the team
            request.user.profile.team = team
            request.user.profile.save()

            return self.account(request)
        else:
            return Response({}, status=_status.HTTP_409_CONFLICT)

    @detail_route(serializer_class=serializers.EmptySerializer)
    def progress(self, *args, **kwargs):
        """Returns a list representing the user's score progression."""

        team = self.get_object()

        return Response(serializers.TeamProfileSerializer(team).data)

    @list_route(permission_classes=[permissions.IsAuthenticated])
    def account(self, request):
        """Displays private information about a user's team."""

        if request.user.profile.team:
            return Response(serializers.AccountSerializer(request.user.profile.team).data)
        else:
            return Response({}, status=_status.HTTP_423_LOCKED)


class UserViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.all()

    @list_route(serializer_class=serializers.EmptySerializer)
    def status(self, request):
        response = {}

        if request.user.is_authenticated():
            response['user'] = serializers.UserSerializer(request.user).data
            response['user']['eligible'] = request.user.profile.eligible

            if request.user.profile.team:
                response['team'] = serializers.TeamProfileSerializer(request.user.profile.team).data

        return Response(response)

    @list_route(methods=['post'], permission_classes=[not_permission(permissions.IsAuthenticated)],
                serializer_class=serializers.UserLoginSerializer)
    def login(self, request):
        """Logs in a user."""

        user = auth.authenticate(username=request.data['username'], password=request.data['password'])

        if user is not None:
            auth.login(request, user)
            return self.status(request)
        else:
            return Response({}, _status.HTTP_401_UNAUTHORIZED)

    @list_route(methods=['post'], permission_classes=[permissions.IsAuthenticated],
                serializer_class=serializers.EmptySerializer)
    def logout(self, request):
        """Logs out a user."""

        auth.logout(request)

        return self.status(request)

    @list_route(methods=['post'], permission_classes=[not_permission(permissions.IsAuthenticated)], serializer_class=serializers.SignupSerializer)
    def signup(self, request):
        """Signs the user up for an account."""

        # Check if this user already exists
        if models.User.objects.filter(username=request.data['username']).exists() or models.User.objects.filter(email=request.data['email']).exists():
            return Response({}, _status.HTTP_409_CONFLICT)

        user = models.User.objects.create_user(request.data['username'],
                                                    email=request.data['email'],
                                                    password=request.data['password'],
                                                    first_name=request.data['first_name'],
                                                    last_name=request.data['last_name'])
        user.is_active = not settings.REQUIRE_USER_ACTIVATION

        user.save()

        # Create user profile
        profile = models.Profile(user=user,
                                 eligible=request.data['profile']['eligible'])

        # Add in optional demographics data
        if request.data['profile']['gender']:
            profile.gender = request.data['profile']['gender']
        if request.data['profile']['race']:
            profile.race = request.data['profile']['race']
        if request.data['profile']['age']:
            profile.age = request.data['profile']['age']
        if request.data['profile']['country']:
            profile.country = request.data['profile']['country']
        if request.data['profile']['state']:
            profile.state = request.data['profile']['state']

        # Generate activation keys
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
        profile.activation_key = hashlib.sha1(salt + request.data['username'].encode('utf8')).hexdigest()
        profile.key_generated = timezone.now()

        profile.save()

        # Log the user in
        user = auth.authenticate(username=user.get_username(), password=request.data['password'])
        auth.login(request, user)

        return self.status(request)

    @detail_route
    def activate(self, request):
        """Activates the user's account."""

        profile = get_object_or_404(models.Profile, activation_key=request.data['key'])

        if not profile.user.is_active:
            if timezone.now() - profile.key_generated > settings.ACTIVATION_EXPIRATION_TIME:
                return Response({
                    'status': 'activation_expired',
                    'user_id': str(profile.user.id)
                }, _status.HTTP_406_NOT_ACCEPTABLE)

        profile.user.is_active = True
        return Response({}, _status.HTTP_200_OK)

    @list_route(methods=['post'], permission_classes=[permissions.IsAuthenticated],
                serializer_class=serializers.UserLoginSerializer)
    def change_password(self, request):
        user = auth.authenticate(username=request.user.get_username(), password=request.data['old'])

        if user is not None:
            user.set_password(request.data['password'])
            user.save()
            auth.login(request, user)
            return Response({})
        else:
            return Response({}, _status.HTTP_401_UNAUTHORIZED)
