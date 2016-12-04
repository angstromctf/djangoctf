from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import Problem, Team, CorrectSubmission, Profile


class ProblemSerializer(serializers.ModelSerializer):
    solved = serializers.SerializerMethodField('is_solved')

    def is_solved(self, obj):
        if 'request' in self.context:
            user = self.context['request'].user
            return user.is_authenticated() and user.profile.team is not None and obj in user.profile.team.solved.all()
        else:
            return False

    class Meta:
        model = Problem
        fields = ('id', 'title', 'text', 'value', 'category', 'hint', 'solved')


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'school', 'score', 'score_lastupdate', 'eligible')


class CorrectSubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    team = TeamSerializer()

    class Meta:
        model = CorrectSubmission
        fields = ('problem', 'team', 'new_score', 'time')


class TeamProfileSerializer(serializers.ModelSerializer):
    solves = CorrectSubmissionSerializer(many=True, read_only=True)
    members = ProfileSerializer(many=True, read_only=True)
    place = serializers.SerializerMethodField()

    def get_place(self, obj):
        place = -1

        for index, team in enumerate(Team.objects.filter(eligible=True)):
            if team.id == obj.id:
                place = index + 1

        return place

    class Meta:
        model = Team
        fields = ('name', 'school', 'score', 'score_lastupdate', 'solves', 'members', 'place')


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('code', 'shell_username', 'shell_password')


class EmptySerializer(serializers.BaseSerializer):
    pass