# Import
import pickle
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from .time import to_minutes, start_time

from ctfapp.globals import GENDER_CHOICES, RACE_CHOICES

# Define core models
class Problem(models.Model):
    """Model for a CTF question. Contains name, title, text, value,
    category, hint, and flag."""
    
    # Outline child models
    problem_name = models.CharField(max_length=200)
    problem_title = models.CharField(max_length=200)
    problem_text = models.TextField()
    problem_value = models.IntegerField()
    problem_category = models.CharField(max_length=50)
    hint_text = models.TextField()
    flag_sha512_hash = models.CharField(max_length=128)
    
    # Convenience
    solved = False

    # Magic methods
    def __str__(self):
        """Represent the problem as a string."""
        return "Problem[" + self.problem_title + "]"


class Update(models.Model):
    """Model for an update message for the CTF. Contains title, text,
    and date."""

    # Outline child models
    update_title = models.CharField(max_length=200)
    update_text = models.CharField(max_length=500)
    date = models.DateTimeField(default=now())

    # Magic methods
    def __str__(self):
        """Represent the update as a string."""
        return repr(self.update_list)


class UserProfile(models.Model):
    """Model for a user registered with the CTF. Contains name,
    school, participation, solved problems, and score data."""
    
    # Linked models
    user = models.OneToOneField(User)
    team = models.ForeignKey('Team', null=True, on_delete=models.SET_NULL)

    # Required information
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    eligible = models.BooleanField(default=True)
    school = models.CharField(max_length=100)

    # Optional demographic information
    gender = models.IntegerField(null=True, choices=GENDER_CHOICES)

    race = models.IntegerField(null=True, choices=RACE_CHOICES)

    # Magic methods
    def __str__(self):
        """Represent the user as a string."""
        return self.user.username

class Team(models.Model):
    """Model for a team registered with the CTF. Contains name,
    school, participation, solved problems, and score data."""
    users = models.ManyToManyField(User)
    user_count = models.IntegerField(default=0)

    school = models.CharField(max_length=100,null=True)

    participating = models.BooleanField(default=True)
    solved = models.BinaryField(default=pickle.dumps({}))

    # Score and last update of the player
    score = models.IntegerField(default=0)
    score_lastupdate = models.DateTimeField(default=now())

class ProblemSolved(models.Model):
    """A model that represents a set of solved problems."""

    # Outline child models
    team = models.ForeignKey(Team)
    new_score = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)

    # Magic methods
    def __str__(self):
        """Represent the solved problem as a string."""
        return "%s solved at %s" % (str(self.team), str(self.minutes))