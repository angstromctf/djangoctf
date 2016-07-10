from django.http import HttpRequest
from django.shortcuts import render
from ctfapp.models import Team
import json


def jsonfeed(request: HttpRequest):

    team_list = Team.objects.filter(score__gt=0).order_by('-score', 'score_lastupdate')

    standings = []
    for team in team_list:
        teamdict = {'team': team.name, 'score': team.score}
        standings.append(teamdict)

    scoreboard = {'standings': standings}
    output_json = json.dumps(scoreboard)

    return render(request, 'jsonfeed.html', {
        'feed_data': output_json
    })

