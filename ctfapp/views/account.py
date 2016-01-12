from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from ctfapp.models import Team

from random import choice

# Create random team code
def create_code():
    return "".join([choice("0123456789abcdef") for x in range(20)])

# Handle the HTTP request
@login_required
def account(request: HttpRequest):
    """Create the account page."""

    render_params = {'change_password': ChangePasswordForm(),
                     'create_team': CreateTeamForm(),
                     'join_team': JoinTeamForm(),
                     'user': request.user}

    if request.method == 'POST':
        create_team = CreateTeamForm(request.POST)

        if create_team.is_valid():
            code = create_code()
            while len(Team.objects.filter(code=code))>0:
                code = create_code()

            team = Team(name=create_team.cleaned_data['name'],
                        user_count=1,
                        school=create_team.cleaned_data['affiliation'],
                        code=code)
            team.save()
            team.users.add(request.user)

            request.user.userprofile.team = team
            request.user.userprofile.save()
        else:
            render_params['create_team'] = create_team

    return render(request, 'account.html', render_params)