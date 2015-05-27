from django.core.exceptions import ValidationError

from ctfapp.models import User

def validate_unique_username(uname):
    users = User.objects.all().filter(username=uname)

    if len(users) > 0:
        raise ValidationError("Team name must be unique.")