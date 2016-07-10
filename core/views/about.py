from django.http import HttpRequest
from django.shortcuts import render
import random

# Name, picture, grade, contributions
people = [
    ("Noah Singer",     "noahsinger.jpg",       10,     "Platform and problems"),
    ("George Klees",    "georgeklees.jpg",      10,     "RE and binary problems"),
    ("Theo Tosini",     "theotosini.jpg",       10,     "Platform, deployment, problems"),
    ("Andrew Komo",     "andrewkomo.jpg",       10,     "Crypto problems"),
    ("Anthony Li",      "anthonyli.jpg",        12,     "Contest organizer"),
    ("Daniel Chen",     "danielchen.jpg",       11,     "PR and outreach"),
    ("Chris Wang",      "chriswang.jpg",        10,     "Art, PR, and outreach"),
    ("Noah Levine",     "noahlevine.jpg",       12,     "Contest organizer"),
    ("Noah Kim",        "noahkim.jpg",          10,     "Website and platform design")
]


def about(request: HttpRequest):
    """Handle a request for the about page."""

    # Compile the list of people and shuffle them
    rand_people = [{"name": _[0], "picture": "/static/images/people/"+_[1], "grade": _[2], "contributions": _[3]} for _ in people]
    random.shuffle(rand_people)

    return render(request, "about.html", {
        "people": rand_people
    })
