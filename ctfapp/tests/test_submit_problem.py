"""
Test submit problem for correct and incorrect solutions
"""
from hashlib import sha512

from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from ..views import submit_problem
from ..models import User, UserProfile, Team, Problem


class SubmitProblemTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        m = sha512()
        m.update(b"flag")
        m.digest()
        hash = m.hexdigest()

        self.problem = Problem(name="problem",
                               title="Problem Title",
                               text="Problem Text",
                               value=100,
                               category="Category",
                               flag_sha512_hash=hash)
        self.problem.save()

        self.no_team_user = User.objects.create_user("noteam",
                                                     email="noteam@email.com",
                                                     password="password",
                                                     first_name="User",
                                                     last_name="Noteam")
        self.no_team_user.is_active = True
        self.no_team_user.userprofile = UserProfile(user=self.no_team_user, eligible=True)
        self.no_team_user.userprofile.save()
        self.no_team_user.save()

        self.team_user = User.objects.create_user("yesteam",
                                                  email="yesteam@email.com",
                                                  password="password",
                                                  first_name="User",
                                                  last_name="Yesteam")

        self.team_user.is_active = True
        self.team_user.userprofile = UserProfile(user=self.team_user, eligible=True)
        self.team_user.userprofile.save()
        self.team_user.save()

        self.team = Team(name="team",
                         user_count=1,
                         school="RRHS",
                         shell_password="",
                         shell_username="",
                         code="",
                         eligible=True)
        self.team.save()
        self.team.users.add(self.team_user)
        self.team_user.userprofile.team = self.team
        self.team_user.userprofile.save()

    def test_anonymous(self):
        """
        Make sure you are redirected to the login page when not logged in
        """
        request = self.factory.post("/problems/submit_problem")
        request.user = AnonymousUser()

        response = submit_problem(request)
        self.assertRedirects(response, "/login")

    def test_no_team(self):
        """
        Make sure you get an exception when you have no team
        """
        request = self.factory.post("/problems/submit_problem")
        request.user = self.no_team_user

        with self.assertRaises(PermissionDenied):
            submit_problem(request)
