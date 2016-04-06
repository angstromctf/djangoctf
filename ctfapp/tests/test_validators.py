"""
Test validators for uniqueness in the test database
"""
from django.core.exceptions import ValidationError
from django.test import TestCase
from ..validators import validate_unique_email, validate_unique_team_name, validate_unique_username
from ..models import User, UserProfile, Team
from ..views.create_team import create_code


class ValidatorTests(TestCase):
    def setUp(self):
        users = []
        for i in range(16):
            user = User.objects.create_user("user{}".format(i),
                                            email="user{:d}@email.com".format(i),
                                            password="password",
                                            first_name="User",
                                            last_name="User{}".format(i))
            user.is_active = True
            user.userprofile = UserProfile(user=user, eligible=True)
            user.userprofile.save()
            user.save()
            users.append(user)

        for i in range(4):
            team = Team(name="team{}".format(i),
                        user_count=1,
                        school="Really Rad High School",
                        shell_username="username{}".format(i),
                        shell_password="password",
                        code=create_code(),
                        eligible=True)
            team.save()
            for j in range(i * 4, i * 4 + 4):
                team.users.add(users[i])
                users[i].userprofile.team = team
                users[i].userprofile.save()

    def test_unique_email(self):
        # It would raise an exception if the email already existed
        validate_unique_email("newemail@e-mail.com")
        with self.assertRaises(ValidationError):
            validate_unique_email("user0@email.com")

    def test_unique_team_name(self):
        validate_unique_team_name("darkside")
        with self.assertRaises(ValidationError):
            validate_unique_team_name("team0")

    def test_unique_username(self):
        validate_unique_username("thetaeo")
        with self.assertRaises(ValidationError):
            validate_unique_username("user0")
