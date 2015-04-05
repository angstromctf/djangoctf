from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import pickle


class Problem(models.Model):
    problem_title = models.CharField(max_length=200)
    problem_text = models.CharField(max_length=500)
    problem_value = models.IntegerField()
    problem_category = models.CharField(max_length=30)
    hint_text = models.CharField(max_length=200)
    flag_sha512_hash = models.CharField(max_length=128)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    school = models.CharField(max_length=100)

    participating = models.BooleanField(default=True)
    solved = models.BinaryField(default=pickle.dumps({}))

    score = models.IntegerField(default=0)
    score_lastupdate = models.DateTimeField(default=datetime.now())

class ProblemSolved(models.Model):
	team = models.ForeignKey(User)
	new_score = models.IntegerField()
	minutes = models.IntegerField()