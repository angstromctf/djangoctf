"""Django CTF competition runtime models.

This module defines two sets of models. Profiles and teams represent
individual competitors and competitor groups. Problems and submissions
objects are the patterns used to store the actual competition content
as well as the progress of the teams.
"""


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


CATEGORIES = [
    'crypto',
    'binary',
    'web',
    're',
    'forensics',
    'misc',
    'master'
]


class Competition(models.Model):
    """A single competition model."""

    name = models.CharField(max_length=60)

    date_registration_start = models.DateTimeField()
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    __current = None
    __current_time = timezone.now()

    @staticmethod
    def current():
        """Get the current or upcoming competition."""

        # "Premature optimization is the root of all evil." - Donald Knuth
        # "Fuck that." - Noah Kim

        # Refresh from cache every 2 hours
        now = timezone.now()
        if Competition.__current is None or (now - Competition.__current_time).seconds > 2 * 60 * 60:
            Competition.__current = Competition.objects.filter(date_end__lte=now).order_by("date_start")
        return Competition.__current


class Profile(models.Model):
    """An expanded user model wrapper.

    The model contains extra information belonging to users, such as
    demographics and teams. Profiles are not subclasses of in order to
    separate CTF related attributes and normal user attributes.
    """

    # Which user this belongs to
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The user's team
    team = models.ForeignKey(
        'Team', blank=True, on_delete=models.SET_NULL, null=True, default=None, related_name='members')

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

    # Magic methods
    def __str__(self):
        """Represent the user as a string."""

        return "Profile[" + self.user.username + "]"


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
        """Represent the problem as a string."""

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
        """Represent the team as a string."""

        return "Team[" + self.name + "]"

    def get_place(self):
        if self.eligible:
            return list(Team.objects.filter(eligible=True)).index(self) + 1
        else:
            return -1

    def report(self):
        """Print a detailed report about this team."""

        return """
        name: {}
        members: {}
        score: {}, place: {}
        eligible: {}
        """.format(self.name,
                   ', '.join(map(lambda member: "{} ({})".format(member.user.get_full_name, member.user.username), self.members.all())),
                   self.score, self.get_place(),
                   self.eligible)


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

    # Magic methods
    def __str__(self):
        """Represent the solved problem as a string."""

        return "%s solved %s at %s" % (str(self.team), str(self.problem), str(self.time))


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
