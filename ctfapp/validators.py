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
        raise ValidationError("Username already exists.")

def validate_unique_team_name(tname):
    """Check if a team name is unique."""
    # Get all team with the specified team name
    teams = Team.objects.all().filter(name=tname)
    # Throw an error if there are any
    if len(teams) > 0:
        raise ValidationError("Team name already exists.")

def validate_team_code(code):
    """Check if a team code is valid."""
    # Get all teams with the specified team code
    teams = Team.objects.all().filter(code=code)

    # Throw an error if the team code wasn't found
    if len(teams) != 1:
        raise ValidationError("Team code not found.")

    team = teams.get(0)

    if team.user_count == 5:
        raise ValidationError("Team is already full.")