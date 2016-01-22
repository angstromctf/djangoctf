from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm

# Handle the HTTP request
@login_required
def account(request: HttpRequest):
    """Create the account page."""

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(),
                                            'join_team': JoinTeamForm(),
                                            'create_team': CreateTeamForm()})