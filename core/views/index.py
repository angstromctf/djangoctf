from django.http import HttpRequest
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from core.utils.time import contest_start, contest_end
from core.decorators import lock_before_contest
from core.models import ProblemUpdate, Team

import json
import random


# Name, picture, grade, contributions
people = [
    ("Noah Singer",     "noahsinger.jpg",       11,     "Platform, learn, problems"),
    ("George Klees",    "georgeklees.jpg",      11,     "RE and binary problems"),
    ("Artemis Tosini",     "theotosini.jpg",       11,     "Platform, deployment, problems"),
    ("Andrew Komo",     "andrewkomo.jpg",       11,     "Crypto problems"),
    ("Daniel Chen",     "danielchen.jpg",       12,     "PR and outreach"),
    ("Chris Wang",      "chriswang.jpg",        11,     "Art, PR, and outreach"),
    ("Noah Kim",        "noahkim.jpg",          11,     "Website and platform design")
]


def index(request: HttpRequest):
    """Handle a request for the index page."""

    return render(request, "index.html", {
        "start": contest_start,
        "end": contest_end
    })


def updates(request):
    """Handles a request for the updates page by sorting and displaying all the updates in the database."""

    updates_list = ProblemUpdate.objects.all().order_by('-time')

    return render(request, 'updates.html', {
        'updates': updates_list
    })


def chat(request):
    """Handle a request for the chat page, which uses the KiwiIRC client."""

    return render(request, "chat.html")


def jsonfeed(request):
    """Constructs a JSON object representing the scoreboard to feed to ctftime."""

    team_list = Team.objects.filter(score__gt=0).order_by('-score', 'score_lastupdate')

    standings = []
    for team in team_list:
        standings.append({'team': team.name, 'score': team.score})

    scoreboard = {'standings': standings}

    return HttpResponse(json.dumps(scoreboard), content_type="application/json")


def about(request):
    """Shuffles and displays the CTF contributors."""

    # Compile the list of people and shuffle them
    rand_people = [{"name": _[0], "picture": "/static/images/people/"+_[1], "grade": _[2], "contributions": _[3]} for _ in people]
    random.shuffle(rand_people)

    return render(request, "about.html", {
        "people": rand_people
    })


def unsubscribe(request):
    """Page that users are redirected to after unsubscribing from the email list."""

    return render(request, "unsubscribe.html")


def sponsors(request):
    """Displays the competition sponsors."""

    return render(request, "sponsors.html")


@login_required
@lock_before_contest
def shelld(request):
    """Displays the online shell."""

    return render(request, "shelld.html")