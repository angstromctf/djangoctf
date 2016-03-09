from django import template
from django.contrib.humanize.templatetags.humanize import ordinal
from ctfapp.models import Team
from ctfapp.utils.time import before_start

register = template.Library()


@register.filter
def is_solved(problem, user):
    return user.is_authenticated() and user.userprofile.team and problem in user.userprofile.team.solved.all()


@register.filter
def place(team):
    for index, item in enumerate(Team.objects.all().order_by('-score', 'score_lastupdate')):
        if item.id == team.id:
            return index+1

    return -1


@register.filter
def possession(name):
    if name[-1] == 's':
        return name + '\''
    return name + '\'s'


@register.filter
def grade_to_name(grade):
    try:
        return ['freshman', 'sophomore', 'junior', 'senior'][grade - 9]
    except IndexError:
        return ordinal(grade) + " Grade"


@register.simple_tag
def contest_started():
    return not before_start()