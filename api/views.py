from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import viewsets, status, schemas
from rest_framework.decorators import detail_route, list_route, api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from api import serializers, models
from api.permissions import ContestStarted, ContestEnded, HasTeam, invert
from api.utils import create_code, create_shell_username, create_shell_password

import hashlib
import logging
import random


logger = logging.getLogger(__name__)


@api_view(exclude_from_schema=True)
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema(request):
    """Retrieve the raw schema view."""

    generator = schemas.SchemaGenerator(title='DjangoCTF API')
    return Response(generator.get_schema())


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    """REST Views for problems."""

    permission_classes = (ContestStarted,)
    queryset = models.Problem.objects.filter(competition__active=True).all()
    serializer_class = serializers.ProblemSerializer

    @detail_route(
        methods=["post"],
        permission_classes=(IsAuthenticated, invert(ContestEnded), HasTeam),
        serializer_class=serializers.ProblemSubmitSerializer)
    def submit(self, request, pk=None) -> Response:
        """Handles problem submissions and returns success status."""

        # Parse post data
        try:
            guess = request.data["guess"].strip().lower()
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Get problem and team
        problem = self.get_object()
        team = request.user.profile.current_team

        # Check if the team has solved
        if problem not in team.solved.all():

            # Check the hash of the guess
            if hashlib.sha512(guess.encode()).hexdigest() == problem.flag:

                # Add problem to solved and update score and time
                team.solved.add(problem)
                team.score += problem.value
                if problem.update_time:
                    team.score_last = timezone.now()
                team.save()

                # Add a new CorrectSubmission object corresponding to having solved the problem
                solution = models.Submission(team=team, problem=problem, new_score=team.score, correct=True)
                solution.save()

            return Response({})

        # The submission was incorrect
        else:

            # Save the response only if they haven't guessed correctly
            if not models.Submission.objects.filter(team=team, problem=problem, correct=True).exists():

                # This is a new incorrect flag
                solution = models.Submission(team=team, problem=problem, guess=guess, correct=False)
                solution.save()

            return Response({}, status=status.HTTP_406_NOT_ACCEPTABLE)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """REST views for teams."""

    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    @list_route(
        methods=['post'],
        permission_classes=(IsAuthenticated, invert(HasTeam)),
        serializer_class=serializers.TeamCreateSerializer)
    def new(self, request):
        """Creates new teams in the competition."""

        # Check if this team already exists
        if models.Team.current(name=request.data['name']).exists():
            return Response({}, status.HTTP_409_CONFLICT)

        code = create_code()
        shell_username = create_shell_username()
        shell_password = create_shell_password()

        # Check if we need to set up a shell account for the team
        if settings.SHELL_ENABLED:
            create_shell_account(shell_username, shell_password)

        # Create the team
        team = models.Team(
            competition=models.Competition.current(),
            name=request.data['name'],
            school=request.data['school'],
            shell_username=shell_username,
            shell_password=shell_password,
            code=code,
            eligible=request.user.profile.eligible)

        try:
            team.full_clean()
        except ValidationError as error:
            return Response({'errors': error.messages}, status=status.HTTP_406_NOT_ACCEPTABLE)

        team.save()
        team.members.add(request.user)

        # Add the user to that team
        request.user.save()

        return self.account(request)

    @list_route(
        methods=['post'],
        permission_classes=(IsAuthenticated, invert(HasTeam)),
        serializer_class=serializers.TeamJoinSerializer)
    def join(self, request):
        """Adds the user to a pre-existing team."""

        team = get_object_or_404(models.Team, code=request.data['code'])
        if team.members.count() < settings.USERS_PER_TEAM:

            # Update team fields
            team.eligible = team.eligible and request.user.profile.eligible
            team.members.add(request.user)
            team.save()
            return self.account(request)

        return Response({}, status=status.HTTP_409_CONFLICT)

    @detail_route(serializer_class=serializers.EmptySerializer)
    def progress(self, *args, **kwargs):
        """Returns a list representing the user's score progression."""

        team = self.get_object()
        return Response(serializers.TeamProfileSerializer(team).data)

    @list_route(permission_classes=[IsAuthenticated])
    def account(self, request):
        """Displays private information about a user's team."""

        team = request.user.profile.current_team
        if team is not None:
            return Response(serializers.ShellAccountSerializer(team).data)
        else:
            return Response({}, status=status.HTTP_423_LOCKED)


class UserViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.all()

    @list_route(serializer_class=serializers.EmptySerializer)
    @method_decorator(ensure_csrf_cookie)
    def status(self, request):
        """Get the current API status (user, team, competition)."""

        current = models.Competition.current()
        response = {'competition': {'start': current.competition_start, 'end': current.competition_end}}
        if request.user.is_authenticated:
            response['user'] = serializers.UserSerializer(request.user).data
            response['user']['eligible'] = request.user.profile.eligible
            if request.user.profile.current_team:
                response['team'] = serializers.TeamProfileSerializer(request.user.profile.current_team).data
        return Response(response)

    @list_route(
        methods=['post'],
        permission_classes=[invert(IsAuthenticated)],
        serializer_class=serializers.UserLoginSerializer)
    def login(self, request):
        """Log in a user."""

        user = auth.authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            auth.login(request, user)
            return self.status(request)
        return Response({}, status.HTTP_401_UNAUTHORIZED)

    @list_route(
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=serializers.EmptySerializer)
    def logout(self, request):
        """Log out a user."""

        auth.logout(request)
        return self.status(request)

    @list_route(
        methods=['post'],
        permission_classes=[invert(IsAuthenticated)],
        serializer_class=serializers.SignupSerializer)
    def signup(self, request):
        """Signs the user up for an account."""

        # Create and save the user
        user = models.User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'])
        user.is_active = not settings.REQUIRE_USER_ACTIVATION

        try:
            user.full_clean()
        except ValidationError as error:
            return Response({'errors': error.messages}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user.save()

        # Create user profile
        profile = models.Profile(
            user=user,
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

        # TODO: compute eligibility posted data instead

        # Generate activation keys
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
        profile.activation_key = hashlib.sha1(salt + request.data['username'].encode('utf8')).hexdigest()
        profile.key_generated = timezone.now()
        profile.save()

        if not settings.REQUIRE_USER_ACTIVATION:
            # Log the user in
            user = auth.authenticate(username=request.data['username'], password=request.data['password'])
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
                }, status.HTTP_406_NOT_ACCEPTABLE)

        profile.user.is_active = True
        return Response({}, status.HTTP_200_OK)

    @list_route(
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=serializers.UserLoginSerializer)
    def change_password(self, request):
        """Change a user's password."""

        user = auth.authenticate(username=request.user.get_username(), password=request.data['old'])
        if user is not None:
            user.set_password(request.data['password'])
            user.save()
            auth.login(request, user)
            return Response({})
        return Response({}, status.HTTP_401_UNAUTHORIZED)


def create_shell_account(shell_username, shell_password):
    import paramiko

    # SSH to shell server
    private_key = paramiko.RSAKey.from_private_key_file(settings.SHELL_PRIVATE_KEY)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=settings.SHELL_HOSTNAME, username='root', pkey=private_key)

    # Create the account
    stdin, stdout, stderr = ssh.exec_command("addctfuser " + shell_username + " " + shell_password)

    stdout_data = stdout.read().decode('utf-8')
    stderr_data = stderr.read().decode('utf-8')

    # Log if something went wrong
    if not stderr:
        logger.error(
            "Error while creating shell account.\nstdout: {}\nstderr: {}".format(stdout_data, stderr_data))
