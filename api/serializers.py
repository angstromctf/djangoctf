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
    """Serializer for when a user joins a team."""

    class Meta:
        model = models.Team
        fields = ('code',)


class UserSerializer(serializers.ModelSerializer):
    """Serialize a user model."""

    class Meta:
        model = models.User
        fields = ('username',)


class UserLoginSerializer(serializers.ModelSerializer):
    """Serializes user login credentials."""

    class Meta:
        model = models.User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    """Serializes all profile and user information."""

    user = UserSerializer()

    class Meta:
        model = models.Profile
        fields = ('user',)


class TeamSerializer(serializers.ModelSerializer):
    """Serializes team information."""

    class Meta:
        model = models.Team
        fields = ('id', 'name', 'school', 'score', 'score_last', 'eligible')


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializes a problem submission for a team."""

    problem = ProblemSerializer()
    team = TeamSerializer()

    class Meta:
        model = models.Submission
        fields = ('problem', 'team', 'new_score', 'time', 'problem', 'team', 'correct')


class TeamProfileSerializer(serializers.ModelSerializer):
    """Serializes team and member information."""

    solves = SubmissionSerializer(many=True, read_only=True)
    members = ProfileSerializer(many=True, read_only=True)
    place = serializers.SerializerMethodField()

    def get_place(self, obj):
        """Get the place in the current competition of the team."""

        place = -1
        for index, team in enumerate(models.Team.objects.filter(eligible=True)):
            if team.id == obj.id:
                place = index + 1
        return place

    class Meta:
        model = models.Team
        fields = ('name', 'school', 'score', 'score_last', 'solves', 'members', 'place')


class ShellAccountSerializer(serializers.ModelSerializer):
    """Serializes the shell account for a team."""

    class Meta:
        model = models.Team
        fields = ('code', 'shell_username', 'shell_password')


class EmptySerializer(serializers.BaseSerializer):
    """Serializes an empty data set."""

    pass


class SignupProfileSerializer(serializers.ModelSerializer):
    """Serializes information from profile registration."""

    class Meta:
        model = models.Profile
        fields = ('eligible', 'country', 'state', 'gender', 'age', 'race')


class SignupSerializer(serializers.ModelSerializer):
    """Serializes core user registration information."""

    profile = SignupProfileSerializer()

    class Meta:
        model = models.User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'profile')
