

from api.models import Team

import random



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