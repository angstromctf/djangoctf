from rest_framework import serializers
from api.models import Problem, Team


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        fields = ('url', 'title', 'text', 'value', 'category', 'hint')


class ProblemSubmitSerializer(serializers.ModelSerializer):
    flag = serializers.Field()

    class Meta:
        model = Problem
        fields = ('flag',)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('url', 'name', 'school', 'score', 'score_lastupdate', 'solved')
        ordering = ('score',)