# Import
from django.core.exceptions import ValidationError
from core.models import User, Team


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
def validate_zip(zipcode):
    """Check if a zip code is five characters long and numeric"""
    first_five = zipcode[:5]
    last_four = zipcode[-4:]
    if len(zipcode) == 5:  # 5-digit zip codes
        if not first_five.isdigit():
            raise ValidationError("Invalid ZIP code entered!")
    else:  # ZIP+4 codes
        if not (first_five.isdigit() and last_four.is_numeric() and (len(zipcode) == 9 or len(zipcode) == 10)):
            raise ValidationError("Invalid ZIP code entered!")
