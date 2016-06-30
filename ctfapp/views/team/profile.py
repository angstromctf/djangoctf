# Import
from django.shortcuts import render, get_object_or_404
from ctfapp.models import Team
from django.utils import timezone

from ctfapp.models import CorrectSubmission
from ctfapp.utils.time import contest_start, minutes


def profile(request, teamid):

    team = get_object_or_404(Team, id=teamid)
    ordered_solves = CorrectSubmission.objects.filter(team=team).order_by("time")

    solutions_list = []

    submissions = CorrectSubmission.objects.all().filter(team=team)

    for sub in submissions:
        delta = sub.time - contest_start

        solutions_list.append([minutes(delta), sub.new_score])


    solutions_list.sort()
    solutions_list.insert(0, [0, 0])
    solutions_list.insert(0, ['X', team.name])

    delta = timezone.now() - contest_start
    solutions_list.append([minutes(delta), team.score])

    return render(request, 'profile.html', {
        'team': team,
        'ordered_solves': ordered_solves,
        'data': str(solutions_list).replace('(', '[').replace(')', ']'),
    })
