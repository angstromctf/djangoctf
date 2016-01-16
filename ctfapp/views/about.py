#The view for the about page. Displays information about angstrom and the project.

from django.http import HttpRequest
from django.shortcuts import render
import random

# PICTURE_STATIC = "http://lorempixel.com/200/200/cats/"
PICTURE_STATIC = "http://i.imgur.com/yaXiDPP.jpg"
# Name, picture, grade, contributions
people = [
    ["Noah Singer",     "noahsinger.jpg",       10,     "Platform and crypto problems, official team movitator"],
    ["George Klees",    "georgeklees.jpg",      10,     "RE and binary problems"],
    ["Theo Tosini",     "theotosini.jpg",       10,     "Platform, deployment, problems"],
    ["Andrew Komo",     "andrewkomo.jpg",       10,     "Crypto"],
    ["Arman Siddique",  "armansiddique.jpg",    10,     ""],
    ["Aaron Szabo",     "aaronszabo.jpg",       12,     ""],
    ["Anthony Li",      "anthonyli.jpg",        12,     "Contest organizer"],
    ["Daniel Chen",     "danielchen.jpg",       11,     "PR and Outreach"],
    ["Chris Wang",      "chriswang.jpg",        10,     "Art, PR, and Outreach"],
    ["Linden Yuan",     "lindenyuan.jpg",       11,     ""],
    ["Noah Levine",     "noahlevine.jpg",       12,     "Contest organizer"],
    ["Noah Kim",        "noahkim.jpg",          10,     "Website and platform design"]
]

# Handle the HTTP request
def about(request: HttpRequest):
    """Create the about page."""
    # Compile the list of people and shuffle them 
    rand_people = [{"name": _[0], "picture": PICTURE_STATIC, "grade": _[2], "contributions": _[3]} for _ in people]
    random.shuffle(rand_people)
    # Return the render
    return render(request, "about.html", {"people": rand_people})
