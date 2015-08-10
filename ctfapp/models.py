from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from ctfapp.time import to_minutes, start_time
import pickle


class Problem(models.Model):
    problem_name = models.CharField(max_length=200)
    problem_title = models.CharField(max_length=200)
    problem_text = models.TextField()
    problem_value = models.IntegerField()
    problem_category = models.CharField(max_length=50)
    hint_text = models.TextField()
    flag_sha512_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.problem_title


class Update(models.Model):
    update_title = models.CharField(max_length=200)
    update_text = models.CharField(max_length=500)
    date = models.DateTimeField(default=now())

    def __str__(self):
        return self.update_list


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    school = models.CharField(max_length=100)

    participating = models.BooleanField(default=True)
    solved = models.BinaryField(default=pickle.dumps({}))

    score = models.IntegerField(default=0)
    score_lastupdate = models.DateTimeField(default=now())

    def __str__(self):
        return self.user.username


class ProblemSolved(models.Model):
    team = models.ForeignKey(User)
    new_score = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)

    def __str__(self):
        return "{:s} solved at {:s}".format(str(self.team), str(self.minutes))