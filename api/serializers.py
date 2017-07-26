"""REST serializers for API models.

Each serializer defines how the respective model is represented whe
it is communicated to the user via the REST API.
"""

from rest_framework import serializers
from . import models


class ProblemSerializer(serializers.ModelSerializer):
    """Serializes the problem model.
    
    Adds a method that indicates whether the problem has been solved
    if the requesting user is logged in and has a team.
    """

    solved = serializers.SerializerMethodField('is_solved')

    def is_solved(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user
            return user.is_authenticated() and user.profile.team is not None and obj in user.profile.team.solved.all()
        else:
            return False

    class Meta:
        model = models.Problem
        fields = ('id', 'title', 'text', 'value', 'category', 'hint', 'solved')


class ProblemSubmitSerializer(serializers.ModelSerializer):
    """Serializes competition problem submission result."""

    flag = serializers.Field()

    class Meta:
        model = models.Problem
        fields = ('flag',)


class TeamCreateSerializer(serializers.ModelSerializer):
    """Serializes team creation result."""

    class Meta:
        model = models.Team
        fields = ('school', 'name')


class TeamJoinSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = models.Team
        fields = ('code',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username',)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Profile
        fields = ('user',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('id', 'name', 'school', 'score', 'score_lastupdate', 'eligible')


class SubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    team = TeamSerializer()

    class Meta:
        model = models.Submission
        fields = ('problem', 'team', 'new_score', 'time', 'problem', 'team', 'correct')


class TeamProfileSerializer(serializers.ModelSerializer):
    solves = SubmissionSerializer(many=True, read_only=True)
    members = ProfileSerializer(many=True, read_only=True)
    place = serializers.SerializerMethodField()

    def get_place(self, obj):
        place = -1

        for index, team in enumerate(models.Team.objects.filter(eligible=True)):
            if team.id == obj.id:
                place = index + 1

        return place

    class Meta:
        model = models.Team
        fields = ('name', 'school', 'score', 'score_lastupdate', 'solves', 'members', 'place')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = ('code', 'shell_username', 'shell_password')


class EmptySerializer(serializers.BaseSerializer):
    pass


class SignupProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = ('eligible', 'country', 'state', 'gender', 'age')


class SignupSerializer(serializers.ModelSerializer):
    profile = SignupProfileSerializer()

    class Meta:
        model = models.User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'profile')