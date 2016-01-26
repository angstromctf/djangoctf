from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from ctfapp.models import UserProfile
# Handle the HTTP request
@login_required
def account(request: HttpRequest):
    """Create the account page."""
    u = request.user
    user_team = u.userprofile.team

    team_member_list = UserProfile.objects.filter(team=user_team)
    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(),
                                            'join_team': JoinTeamForm(),
                                            'team_member_list': team_member_list,
                                            'create_team': CreateTeamForm()})