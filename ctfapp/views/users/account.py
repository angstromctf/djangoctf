from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from ctfapp.models import UserProfile
# Handle the HTTP request


@login_required
def account(request: HttpRequest):
    """Create the account page."""

    user_team = request.user.userprofile.team
    team_member_list = UserProfile.objects.filter(team=user_team)

    return render(request, 'account.html', {
        'user': request.user,
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'team_member_list': team_member_list,
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })
