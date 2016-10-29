from django.utils import timezone

from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.models import Problem, Team, CorrectSubmission, IncorrectSubmission
from api.permissions import ContestStarted, ContestEnded, HasTeam, not_permission
from api.serializers import ProblemSerializer, TeamSerializer, ProblemSubmitSerializer

import hashlib


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ContestStarted,)
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    @detail_route(methods=['post'], permission_classes=(permissions.IsAuthenticated, not_permission(ContestEnded),
                                                        HasTeam), serializer_class=ProblemSubmitSerializer)
    def submit(self, request, *args, **kwargs):
        """Handles submissions for specific problems and returns success status."""

        problem = self.get_object()
        team = request.user.profile.team

        guess = request.data['flag'].strip().lower()

        response = {}

        if problem in team.solved.all():
            response['status'] = 'already_solved'
        elif hashlib.sha512(guess.encode()).hexdigest() == problem.flag:
            # We have now solved the problem because the solution was correct
            team.solved.add(problem)

            # Update the team's score
            team.score += problem.value

            if problem.update_time:
                team.score_lastupdate = timezone.now()

            team.save()

            # Add a new CorrectSubmission object corresponding to having solved the problem
            solution = CorrectSubmission(team=team, problem=problem, new_score=team.score)
            solution.save()

            response['status'] = 'correct'
        else:
            if IncorrectSubmission.objects.filter(team=team, problem=problem, guess=guess).count() > 0:
                response['already_attempted'] = True
            else:
                solution = IncorrectSubmission(team=team, problem=problem, guess=guess)
                solution.save()
                response['already_attempted'] = False

            response['status'] = 'incorrect'

        return Response(response)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
