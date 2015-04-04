from django.db import models

class Problem(models.Model):
	problem_title = models.CharField(max_length=200)
	problem_text = models.CharField(max_length=200)
	problem_value = models.IntegerField()
	hint_text = models.CharField(max_length=200)
	flag_text = models.CharField(max_length=200)
