# Import
from django.shortcuts import render
from ctfapp.models import Team
from django.http import Http404

from ctfapp.models import CorrectSubmission

def profile(request, team):
    try:
        team = Team.objects.get(name=team)
    except Team.DoesNotExist:
        raise Http404('No team with name ' + team + ' exists.')

    ordered_solves = CorrectSubmission.objects.filter(team=team).order_by("time")

    return render(request, 'profile.html', {
        'team': team,
        'ordered_solves': ordered_solves
    })
