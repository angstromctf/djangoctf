"""Django CTF competition runtime models.

This module defines two sets of models. Profiles and teams represent
individual competitors and competitor groups. Problems and submissions
objects are the patterns used to store the actual competition content
as well as the progress of the teams.
"""


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms import ValidationError

CATEGORIES = ['crypto', 'binary', 'web', 're', 'forensics', 'misc', 'master']


class Competition(models.Model):
    """A single competition model."""

    name = models.CharField(max_length=60)
    active = models.BooleanField(default=False)

    registration_start = models.DateTimeField()
    competition_start = models.DateTimeField()
    competition_end = models.DateTimeField()

    def save(self, *args, **kwargs):
        """Save and make sure there is only one active competition."""

        if self.active:
            for competition in Competition.objects.filter(active=True).exclude(id=self.id):
                competition.active = False
                competition.save()
        super(Competition, self).save()

    def can_register(self):
        """Check if a user can register at the current time."""

        return self.registration_start < timezone.now() < self.competition_end

    def can_compete(self):
        """Check if a user can compete at the current time."""

        return self.competition_start < timezone.now() < self.competition_end

    def has_started(self):
        """Check if the contest has started."""

        return self.competition_start < timezone.now()

    def has_ended(self):
        """Check if the competition has ended."""

        return self.competition_end < timezone.now()

    @staticmethod
    def current() -> "Competition":
        """Get the current or upcoming competition."""

        try:
            return Competition.objects.get(active=True)
        except Competition.DoesNotExist:
            return None


class Profile(models.Model):
    """An expanded user model wrapper.

    The model contains extra information belonging to users, such as
    demographics and teams. Profiles are not subclasses of in order to
    separate CTF related attributes and normal user attributes.
    """

    # Which user this belongs to
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Activation information for this user
    activation_key = models.CharField(max_length=40, blank=True, null=True, default="")
    key_generated = models.DateTimeField(default=timezone.now)

    # Required information
    eligible = models.BooleanField(default=False)

    # Optional demographic information
    gender = models.TextField(blank=True, null=True)
    race = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Profile[" + self.user.username + "]"

    @property
    def current_team(self):
        try:
            return self.user.teams.get(competition__active=True)
        except Team.DoesNotExist:
            return None


class Problem(models.Model):
    """A CTF problem with information."""

    # Competition
    competition = models.ForeignKey(Competition, related_name="problems", on_delete=models.CASCADE)

    # Standard information about the problem
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    value = models.IntegerField()
    category = models.CharField(max_length=50)
    hint = models.TextField()

    # Hash the flags so attackers can't get them even with database access
    flag = models.CharField(max_length=128)

    def __str__(self):
        return "Problem[" + self.title + "]"

    class Meta:
        ordering = ('value',)

    # def save(self, *args, **kwargs):
    #     try:
    #         old_value = Problem.objects.get(id=self.id).value
    #
    #         if self.value != old_value:
    #             delta = self.value - old_value
    #
    #             for team in Team.objects.filter(solved=self):
    #                 team.score += delta
    #                 team.save()
    #
    #                 correct = CorrectSubmission.objects.get(team=team, problem=self)
    #                 for submission in CorrectSubmission.objects.filter(team=team):
    #                     if submission.time >= correct.time:
    #                         submission.new_score += delta
    #                         submission.save()
    #     except Problem.DoesNotExist:
    #         pass
    #
    #     super(Problem, self).save(*args, **kwargs)


class Team(models.Model):
    """A team registered with the CTF.

    Teams track unique identity as well as progression throughout the
    current competition. Teams do contain have a defined reference to
    team member profile models; these can be accessed instead by
    reverse calls to the members attribute.
    """

    # Competition
    competition = models.ForeignKey(Competition, related_name="teams", on_delete=models.CASCADE)

    # Team members
    members = models.ManyToManyField(User, related_name="teams")

    # Which problems this team has solved
    solved = models.ManyToManyField(Problem, blank=True, related_name="solvers")

    # Information about team
    name = models.CharField(max_length=64)
    school = models.CharField(max_length=64)
    eligible = models.BooleanField(default=True)

    address_street = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_street_line_2 = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_zip = models.CharField(max_length=10, default=None, null=True, blank=True)
    address_city = models.CharField(max_length=1000, default=None, null=True, blank=True)
    address_state = models.CharField(max_length=1000, default=None, null=True, blank=True)

    # Code for team registration
    code = models.CharField(max_length=20)

    # Score and last update of the team
    score = models.IntegerField(default=0)
    score_last = models.DateTimeField(default=timezone.now)

    # Shell username and password
    shell_username = models.CharField(max_length=20, default="")
    shell_password = models.CharField(max_length=50, default="")

    # Meta model attributes
    class Meta:
        ordering = ("-score", "score_last")

    def __str__(self):
        return "Team[" + self.name + "]"

    def clean(self):
        """Validate fields in the model.

        Namely, make sure that no members on this team are part of
        another team for the same competition. This is possible
        because membership is managed through a many to many.
        """

        # TODO: make sure there are checks for team membership

        for member in self.members.all():
            if member.teams.filter(competition=self.competition).exclude(id=self.id).exists():
                raise ValidationError("Some team members already part of a team.")
        super().clean()

    def get_place(self):
        """Get the place of the team in the current competition."""

        if self.eligible:
            return list(Team.objects.filter(eligible=True, competition__active=True)).index(self) + 1
        return -1

    @staticmethod
    def current(**kwargs):
        """Filter active competitions."""

        return Team.objects.filter(competition__active=True, **kwargs)


class Submission(models.Model):
    """A correct submission for a problem."""

    # Link to team and problem
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='solves')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solves')

    # Time and correctness
    time = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField()

    # Guess and new score
    guess = models.CharField(max_length=128, default="")
    new_score = models.IntegerField(default=0)

    class Meta:
        ordering = ('time',)

    def __str__(self):
        return "{} solved {} at {}".format(self.team, self.problem, self.time)


# class ProblemUpdate(models.Model):
#     """An update to a problem."""
#
#     # Link to problem
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
#
#     # Update information
#     text = models.CharField(max_length=256)
#     time = models.DateTimeField(default=timezone.now)
#
#     # Magic methods
#     def __str__(self):
#         return "%s updated at %s: %s" % (str(self.problem), str(self.time), str(self.time))


# class Sponsor(models.Model):
#     """A company or organization who sponsored this competition."""
#
#     # Company information
#     name = models.CharField(max_length=256)
#     text = models.TextField()
