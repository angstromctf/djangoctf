# Import
from django.core.exceptions import ValidationError
from ctfapp.models import User, Team

# System wide validators
def validate_unique_username(uname):
    """Check if a username is unique."""
    # Get all users with the specified username
    users = User.objects.all().filter(username=uname)
    # Throw an error if there are any
    if len(users) > 0:
        raise ValidationError("Username must be unique.")

def validate_unique_team_name(tname):
    """Check if a team name is unique."""
    # Get all team with the specified team name
    teams = Team.objects.all().filter(name=tname)
    # Throw an error if there are any
    if len(teams) > 0:
        raise ValidationError("Team name must be unique.")