# Import
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from ctfapp.utils.globals import GENDER_CHOICES, RACE_CHOICES

"""
Various core database models for angstrom.
"""


class Problem(models.Model):
    """Model for a CTF question. Contains name, title, text, value,
    category, hint, and flag."""
    
    # Standard information about the problem
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    value = models.IntegerField()
    category = models.CharField(max_length=50)

    hint_text = models.TextField()
    flag_sha512_hash = models.CharField(max_length=128)

    # Whether solving this problem should update a team's "last submitted" time
    # Only should be off for things like survey problems
    update_time = models.BooleanField(default=True)

    # Magic methods
    def __str__(self):
        """Represent the problem as a string."""
        return "Problem[" + self.title + "]"


class Update(models.Model):
    """Model for an update message for the CTF. Contains title, text,
    and date."""
    
    # Information about an update
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    time = models.DateTimeField(default=timezone.now)

    # Magic methods
    def __str__(self):
        """Represent the update as a string."""
        return "Update[" + self.title + "]"


class UserProfile(models.Model):
    """Model for a user registered with the CTF. Contains name,
    school, participation, solved problems, and score data."""
    
    # Which user this belongs to
    user = models.OneToOneField(User)

    # The user's team
    team = models.ForeignKey('Team', blank=True, on_delete=models.SET_NULL, null=True, default=None)

    # Activation information for this user
    activation_key = models.CharField(max_length=40, default="")
    key_generated = models.DateTimeField(default=timezone.now)

    # Required information
    eligible = models.BooleanField(default=True)

    # Optional demographic information
    gender = models.IntegerField(blank=True, choices=GENDER_CHOICES, null=True)
    race = models.IntegerField(blank=True, choices=RACE_CHOICES, null=True)
    age = models.IntegerField(blank=True, null=True)

    # Magic methods
    def __str__(self):
        """Represent the user as a string."""
        return self.user.username


class Team(models.Model):
    """Model for a team registered with the CTF. Contains name,
    school, participation, solved problems, score data, and shell
    login info. """

    # Link to team members
    users = models.ManyToManyField(User)

    # Which problems this team has solved
    solved = models.ManyToManyField(Problem)

    # Information about team
    name = models.CharField(max_length=100)
    user_count = models.IntegerField(default=0)
    school = models.CharField(max_length=100)
    eligible = models.BooleanField(default=True)

    # Code for team registration
    code = models.CharField(max_length=20)

    # Score and last update of the team
    score = models.IntegerField(default=0)
    score_lastupdate = models.DateTimeField(default=timezone.now)

    # Shell username and password
    shell_username = models.CharField(max_length=20, default="")
    shell_password = models.CharField(max_length=50, default="")

    # Magic methods
    def __str__(self):
        """Represent the problem as a string."""
        return "Team[" + self.name + "]"


class CorrectSubmission(models.Model):
    """A model that represents a correct submission for a problem."""

    # Link to team and problem
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)

    # Team's score at that time
    new_score = models.IntegerField(default=0)
    time = models.DateTimeField(default=timezone.now)

    # Magic methods
    def __str__(self):
        """Represent the solved problem as a string."""
        return "%s solved %s at %s" % (str(self.team), str(self.problem), str(self.time))


class IncorrectSubmission(models.Model):
    """A model that represents an incorrect submission for a problem."""

    # Link to team and problem
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)

    # Time and contents of submission
    guess = models.CharField(max_length=64)
    time = models.DateTimeField(default=timezone.now)

    # Magic methods
    def __str__(self):
        """Represent the solved problem as a string."""
        return "%s incorrectly submitted %s at %s" % (str(self.team), str(self.problem), str(self.time))
