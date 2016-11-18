from django.conf import settings
from django.contrib import auth
from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from api import serializers, models
from api.permissions import ContestStarted, ContestEnded, HasTeam, not_permission
from api.utils import create_code, create_shell_username, create_shell_password

import hashlib
import logging

logger = logging.getLogger(__name__)


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ContestStarted,)
    queryset = models.Problem.objects.all()
    serializer_class = serializers.ProblemSerializer

    @detail_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(ContestEnded),
                                                        HasTeam), serializer_class=serializers.ProblemSubmitSerializer)
    def submit(self, request):
        """Handles submissions for specific problems and returns success status."""

        problem = self.get_object()
        team = request.user.profile.team
        guess = request.data['flag'].strip().lower()

        response = {}

        code = status.HTTP_200_OK

        # We've already solved this problem
        if problem in team.solved.all():
            response['status'] = 'already_solved'

        # We've now solved the problem because the solution was correct
        elif hashlib.sha512(guess.encode()).hexdigest() == problem.flag:
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

            response['status'] = 'correct'

        # The submission was incorrect
        else:
            code = status.HTTP_406_NOT_ACCEPTABLE

            if models.IncorrectSubmission.objects.filter(team=team, problem=problem, guess=guess).count() > 0:
                # The user has already attempted this incorrect flag
                response['already_attempted'] = True
            else:
                # This is a new incorrect flag
                solution = models.IncorrectSubmission(team=team, problem=problem, guess=guess)
                solution.save()
                response['already_attempted'] = False

            response['status'] = 'incorrect'

        return Response(response)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(HasTeam)),
                serializer_class=serializers.TeamCreateSerializer)
    def new(self, request):
        """Creates new teams for the competition."""

        code = create_code()
        shell_username = create_shell_username()
        shell_password = create_shell_password()

        # Check if we need to set up a shell account for the team
        if settings.CONFIG['shell']['enabled']:
            import paramiko

            # SSH to shell server
            private_key = paramiko.RSAKey.from_private_key_file(settings.CONFIG['shell']['ssh_key_path'])
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=settings.CONFIG['shell']['hostname'], username='root', pkey=private_key)

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

        response = {
            'code': code
        }

        return Response(response)

    @list_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(HasTeam)),
                serializer_class=serializers.TeamJoinSerializer)
    def join(self, request):
        """Adds the user to a pre-existing team."""

        team = models.Team.objects.get(code=request.data['code'])

        # Compute the team's eligibility by combining its current eligibility with the user's eligibility
        team.eligible = team.eligible and request.user.profile.eligible
        team.save()

        response = {}

        if team.members.count() < settings.CONFIG['users_per_team']:
            # If there are fewer than max number of people on the team, add the user to the team
            request.user.profile.team = team
            request.user.profile.save()

        return Response(response)

    @detail_route(serializer_class=serializers.TeamProgressSerializer)
    def progress(self, request, *args, **kwargs):
        """Returns a list representing the user's score progression."""
        return self.list(request, *args, **kwargs)


class UserViewSet(viewsets.GenericViewSet):
    queryset = auth.models.User.objects.all()

    @list_route(methods=['post'], permission_classes=[not_permission(permissions.IsAuthenticated)],
                serializer_class=serializers.UserLoginSerializer)
    def login(self, request):
        """Logs in a user."""

        user = auth.authenticate(username=request.data['username'], password=request.data['password'])

        if user is not None:
            auth.login(request, user)
            code = status.HTTP_200_OK
        else:
            code = status.HTTP_401_UNAUTHORIZED

        return Response(status=code)

    @list_route(permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Logs out a user."""
        auth.logout(request)

        return Response(status=status.HTTP_200_OK)

    @list_route(permission_classes=[permissions.IsAuthenticated], renderer_classes=[JSONRenderer])
    def account(self, request):
        """Displays private information about a user's team."""
        response = {}

        if request.user.profile.team:
            return Response(serializers.AccountSerializer(request.user.profile.team).data)
        else:
            return Response(status=status.HTTP_423_LOCKED)