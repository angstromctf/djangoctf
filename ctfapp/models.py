from django.db import models

class Problem(models.Model):
	problem_title = models.CharField(max_length=200)
	problem_text = models.CharField(max_length=500)
	problem_value = models.IntegerField()
	problem_category = models.CharField(max_length=30)
	hint_text = models.CharField(max_length=200)
	flag_sha512_hash = models.CharField(max_length=128)
