from django.shortcuts import render

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


def about(request):
    """Shuffles and displays the CTF contributors."""

    # Compile the list of people and shuffle them
    rand_people = [{"name": _[0], "picture": "/static/images/people/"+_[1], "grade": _[2], "contributions": _[3]} for _ in people]
    random.shuffle(rand_people)

    return render(request, "about.html", {
        "people": rand_people
    })
