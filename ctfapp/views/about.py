from django.http import HttpRequest
from django.shortcuts import render
from random import shuffle

people = [
    # Name               Picture          Grade Contributions
    ['Noah Singer', 'noahsinger.jpg', 9, 'Platform and crypto problems'],
    ['George Klees', 'georgeklees.jpg', 9, 'RE and binary problems'],
    ['Artemis Tosini', 'theotosini.jpg', 9, 'Platform, deployment, problems'],
    ['Andrew Komo', 'andrewkomo.jpg', 9, 'Many crypto problems'],
    ['Aaron Szabo', 'aaronszabo.jpg', 11, '???'],
    ['Akash Canjels', 'akashcanjels.jpg', 9, '???'],
    ['Anthony Li', 'anthonyli.jpg', 11, 'Contest organizer'],
    ['Daniel Chen', 'danielchen.jpg', 10, '???'],
    ['Linden Yuan', 'lindenyuan.jpg', 10, '???'],
    ['Noah Levine', 'noahlevine.jpg', 11, 'Contest organizer'],
    ['Noah Kim', 'noahkim.jpg', 9, 'Website Design']
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
