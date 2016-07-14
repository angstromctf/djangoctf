from django.http import HttpResponse

from core.models import Team

import json


def jsonfeed(request):
    """Constructs a JSON object representing the scoreboard to feed to ctftime."""

    team_list = Team.objects.filter(score__gt=0).order_by('-score', 'score_lastupdate')

    standings = []
    for team in team_list:
        standings.append({'team': team.name, 'score': team.score})

    scoreboard = {'standings': standings}

    return HttpResponse(json.dumps(scoreboard), content_type="application/json")

