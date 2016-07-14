from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from core.models import CorrectSubmission, Team
from core.utils.time import contest_start, contest_end, minutes


def profile(request, team_id):
    """Displays basic information and score progression for a given team."""

    team = get_object_or_404(Team, id=team_id)

    # Sort the problems this team has solved
    ordered_solves = CorrectSubmission.objects.filter(team=team).order_by("time")

    # Graph the score progression of this team
    solutions_list = []

    submissions = CorrectSubmission.objects.all().filter(team=team)

    for sub in submissions:
        delta = sub.time - contest_start

        solutions_list.append([minutes(delta), sub.new_score])

    solutions_list.sort()
    solutions_list.insert(0, [0, 0])
    solutions_list.insert(0, ['X', team.name])

    delta = min(timezone.now(), contest_end) - contest_start
    solutions_list.append([minutes(delta), team.score])

    return render(request, 'profile.html', {
        'team': team,
        'ordered_solves': ordered_solves,
        'data': str(solutions_list).replace('(', '[').replace(')', ']'),
    })
