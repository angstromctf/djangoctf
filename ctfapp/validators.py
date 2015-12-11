# Import
from django.core.exceptions import ValidationError
from ctfapp.models import User

# System wide validators
def validate_unique_username(uname):
    """Check if a username is unique."""
    # Get all users with the specified username
    users = User.objects.all().filter(username=uname)
    # Throw an error if there are any
    if len(users) > 0:
        raise ValidationError("Team name must be unique.")