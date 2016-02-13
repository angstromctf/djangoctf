# Import
from django.shortcuts import render
from ctfapp.models import Team
from django.http import Http404
from django.utils.timezone import now

from ctfapp.models import CorrectSubmission
from ctfapp.utils.time import contest_start, minutes

def profile(request, team):
    try:
        team = Team.objects.get(name=team)
    except Team.DoesNotExist:
        raise Http404('No team with name ' + team + ' exists.')

    ordered_solves = CorrectSubmission.objects.filter(team=team).order_by("time")

    solutions_list = []
    graph_size = min(5, Team.objects.all().count())

    for x in range(graph_size):
        submissions = CorrectSubmission.objects.all().filter(team=team)

        for sub in submissions:
            delta = sub.time - contest_start

            solutions_list.append([minutes(delta)] + [-1] * x + [sub.new_score] + [-1] * (graph_size-1-x))


    solutions_list.sort()
    solutions_list.insert(0, [0, 0])
    solutions_list.insert(0, ['X', team.name])

    delta = now() - contest_start
    solutions_list.append([minutes(delta), team.score])

    return render(request, 'profile.html', {
        'team': team,
        'ordered_solves': ordered_solves,
        'data': str(solutions_list).replace('-1', 'null').replace('(', '[').replace(')', ']'),
    })
