from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from api.models import Team

import random


contest_start = parse_datetime(settings.START_TIME)
contest_end = parse_datetime(settings.END_TIME)


def before_start():
    return timezone.now() < contest_start


def after_end():
    return timezone.now() > contest_end


def minutes(delta):
    return delta.days * 1440 + delta.seconds // 60


# Creates a random team code
def create_code():
    code = "".join([random.choice("0123456789abcdef") for x in range(20)])

    if Team.objects.filter(code=code).count() > 0:
        return create_code()

    return code


# Generates a random shell username
def create_shell_username():
    shell_username = "team" + "".join([random.choice("0123456789") for x in range(6)])

    if Team.objects.filter(shell_username=shell_username).count() > 0:
        return create_shell_username()

    return shell_username


# Generates a random shell password
def create_shell_password():
    return "".join([random.choice("0123456789abcdef") for x in range(12)])