from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import Problem, Team, CorrectSubmission, Profile


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    solved = serializers.SerializerMethodField('is_solved')

    def is_solved(self, obj):
        user = self.context['request'].user
        return user.is_authenticated() and user.profile.team is not None and obj in user.profile.team.solved

    class Meta:
        model = Problem
        fields = ('url', 'title', 'text', 'value', 'category', 'hint', 'solved')


class ProblemSubmitSerializer(serializers.ModelSerializer):
    flag = serializers.Field()

    class Meta:
        model = Problem
        fields = ('flag',)


class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('school', 'name')


class TeamJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('code',)


class SubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()

    class Meta:
        model = CorrectSubmission
        fields = ('problem', 'time')


class TeamProgressSerializer(serializers.ModelSerializer):
    solves = SubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('solves',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user',)


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    members = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('url', 'name', 'school', 'score', 'score_lastupdate', 'id', 'solved', 'members')
        ordering = ('score',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('code', 'shell_username', 'shell_password')


class EmptySerializer(serializers.BaseSerializer):
    pass