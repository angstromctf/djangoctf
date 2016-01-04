from django import template
from django.contrib.humanize.templatetags.humanize import ordinal
from ctfapp.models import UserProfile

register = template.Library()


@register.filter
def is_solved(problem, solved):
    return (problem.id in solved) and solved[problem.id][0]


@register.filter
def try_count(problem, solved):
    return solved[problem.id][1] if problem.id in solved else 1


@register.filter
def place(user):
    for index, item in enumerate(UserProfile.objects.all().order_by('-score', 'score_lastupdate')):
        if item.user.id == user.id:
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
