from rest_framework import serializers
from api.models import Problem, Team


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ('url', 'title', 'text', 'value', 'category', 'hint')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'school', 'score', 'score_lastupdate', 'solved')