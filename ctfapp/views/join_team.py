from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from ctfapp.models import Team
from ctfapp.decorators import team_required

# Handle the HTTP request
@login_required
@team_required(invert=True)
def join_team(request: HttpRequest):
    """Create the account page."""

    if request.method == 'POST':
        join_team = JoinTeamForm(request.POST)

        if join_team.is_valid():
            team = Team.objects.get(code=join_team.cleaned_data['code'])
            team.user_count += 1
            team.eligible = team.eligible and request.user.userprofile.eligible

            team.save()
            team.users.add(request.user)

            print(type(request.user.userprofile))
            request.user.userprofile.team = team
            request.user.userprofile.save()
    else:
        join_team = JoinTeamForm()

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(),
                                            'join_team': join_team,
                                            'create_team': CreateTeamForm()})