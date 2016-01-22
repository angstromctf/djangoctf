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
def create_team(request: HttpRequest):
    """Create the account page."""

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
        create_team = CreateTeamForm()

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(),
                                            'join_team': JoinTeamForm(),
                                            'create_team': create_team})