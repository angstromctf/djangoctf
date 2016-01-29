from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from ctfapp.models import UserProfile
# Handle the HTTP request

@login_required
def account(request: HttpRequest):
    """Create the account page."""

    not_activated_err = """Your account has not been activated! Please click the activation link
                            sent via email to verify your account."""
    if not request.user.is_active:
        return render(request, 'message_generic.html', {'message': not_activated_err})
    else:
        user_team = request.user.userprofile.team
        team_member_list = UserProfile.objects.filter(team=user_team)
        return render(request, 'account.html', {'user': request.user,
                                                'change_password': ChangePasswordForm(),
                                                'join_team': JoinTeamForm(),
                                                'team_member_list': team_member_list,
                                                'create_team': CreateTeamForm()})