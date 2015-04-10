from django.http import HttpRequest
from django.shortcuts import render
from random import shuffle

people = [
    # Name               Picture          Grade Contributions
    ['Noah Singer',     'noahsinger.jpg',   9,  'Extensive contributions to the platform and crypto problems'],
    ['George Klees',    'georgeklees.jpg',  9,  'Reverse engineering and binary exploitation problems'],
    ['Theo Tosini',     'theotosini.jpg',   9,  'Extensive contributions to platform and deployment, and some misc and web problems'],
    ['Andrew Komo',     'andrewkomo.jpg',   9,  'Many crypto problems'],
    ['Noah Kim',        'noahkim.jpg',      9,  'Contributions to platform and problems']
]
PICTURE_STATIC = 'http://lorempixel.com/200/200/cats/'


def about(request: HttpRequest):
    rand_people = [{'name': _[0],
                    'picture': PICTURE_STATIC,
                    'grade': _[2],
                    'contributions': _[3]} for _ in people]
    shuffle(rand_people)

    return render(request, "about.html", {
        'people': rand_people
    })