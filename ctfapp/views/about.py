from django.http import HttpRequest
from django.shortcuts import render
from random import shuffle

people = [
    # Name               Picture          Grade Contributions
    ['Noah Singer', 'noahsinger.jpg', 10, 'Platform and crypto problems, official team movitator'],
    ['George Klees', 'georgeklees.jpg', 10, 'RE and binary problems'],
    ['Artemis Tosini', 'theotosini.jpg', 10, 'Platform, deployment, problems'],
    ['Andrew Komo', 'andrewkomo.jpg', 10, 'ALL THE CRYPTO'],
    ['Arman Siddique', 'armansiddique.jpg', 10, 'Being god'],
    ['Aaron Szabo', 'aaronszabo.jpg', 12, '???'],
    ['Anthony Li', 'anthonyli.jpg', 12, 'Contest organizer'],
    ['Daniel Chen', 'danielchen.jpg', 11, 'PR and Outreach'],
    ['Chris Wang', 'chriswang.jpg', 10, 'Art, PR, and Outreach'],
    ['Linden Yuan', 'lindenyuan.jpg', 11, '???'],
    ['Noah Levine', 'noahlevine.jpg', 12, 'Contest organizer'],
    ['Noah Kim', 'noahkim.jpg', 10, 'Website Design']
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
