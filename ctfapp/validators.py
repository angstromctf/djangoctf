# Import
from django.core.exceptions import ValidationError
from ctfapp.models import User, Team

# System wide validators
def validate_unique_username(uname):
    """Check if a username is unique."""
    # Get all users with the specified username
    users = User.objects.all().filter(username=uname)

    # Throw an error if there are any
    if users.count() > 0:
        raise ValidationError("Username already exists.")

def validate_unique_team_name(tname):
    """Check if a team name is unique."""
    # Get all team with the specified team name
    teams = Team.objects.all().filter(name=tname)

    # Throw an error if there are any
    if teams.count() > 0:
        raise ValidationError("Team name already exists.")

def validate_unique_email(email_address):
    """Check if an email address is unique."""
    # Get all users with the specified email address
    users = User.objects.all().filter(email=email_address)

    # Throw an error if there are any
    if users.count() > 0:
        raise ValidationError("Email address already registered.")