from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from core.utils.globals import GENDER_CHOICES, RACE_CHOICES, ELIGIBLE_CHOICES


class Problem(models.Model):
    """A CTF problem with information."""
    
    # Standard information about the problem
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    value = models.IntegerField()
    category = models.CharField(max_length=50)
    hint_text = models.TextField()

    # Hash the flags so attackers can't get them even with database access
    flag_sha512_hash = models.CharField(max_length=128)

    # Whether solving this problem should update a team's "last submitted" time (off for survey problems)
    update_time = models.BooleanField(default=True)

    # Magic methods
    def __str__(self):
        """Represent the problem as a string."""
        return "Problem[" + self.title + "]"

    def save(self, *args, **kwargs):
        try:
            old_value = Problem.objects.get(id=self.id).value

            if self.value != old_value:
                delta = self.value - old_value

                for team in Team.objects.filter(solved=self):
                        team.score += delta
                        team.save()

                        correct = CorrectSubmission.objects.get(team=team, problem=self)
                        for submission in CorrectSubmission.objects.filter(team=team):
                            if submission.time >= correct.time:
                                submission.new_score += delta
                                submission.save()
        except Problem.DoesNotExist:
            pass

        super(Problem, self).save(*args, **kwargs)


class Profile(models.Model):
    """Extra information belonging to users, such as demographics and teams, in addition to normal Django User model."""
    
    # Which user this belongs to
    user = models.OneToOneField(User)

    # The user's team
    team = models.ForeignKey('Team', blank=True, on_delete=models.SET_NULL, null=True,
                             default=None, related_name="profiles")

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
    """A team registered with the CTF. Contains identity and tracks problems solved and score. """

    # Which problems this team has solved
    solved = models.ManyToManyField(Problem, related_name="solvers")

    # Information about team
    name = models.CharField(max_length=128)
    school = models.CharField(max_length=128)

    eligible = models.BooleanField(default=True)
    eligible2 = models.IntegerField(blank=True, choices=ELIGIBLE_CHOICES, null=True)

    address_street = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_street_line_2 = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_zip = models.CharField(max_length=10, default=None, null=True, blank=True)
    address_city = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_state = models.CharField(max_length=1000, default=None, null=True, blank=True)

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
    """A correct submission for a problem."""

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
    """An incorrect submission for a problem."""

    # Link to team and problem
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)

    # Time and contents of submission
    guess = models.CharField(max_length=128)
    time = models.DateTimeField(default=timezone.now)

    # Magic methods
    def __str__(self):
        """Represent the solved problem as a string."""
        return "%s incorrectly submitted %s at %s" % (str(self.team), str(self.problem), str(self.time))


class ProblemUpdate(models.Model):
    """An update to a problem."""

    # Link to problem
    problem = models.ForeignKey(Problem)

    # Update information
    text = models.CharField(max_length=256)
    time = models.DateTimeField(default=timezone.now)

    # Magic methods
    def __str__(self):
        return "%s updated at %s: %s" % (str(self.problem), str(self.time), str(self.time))

class Sponsor(models.Model):
    """A company or organization who sponsored this competition."""

    # Company information
    name = models.CharField(max_length=256)
    text = models.TextField()

