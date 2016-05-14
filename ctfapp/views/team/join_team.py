from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse

from ctfapp.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm
from ctfapp.models import Team
from ctfapp.decorators import team_required


# Handle the HTTP request
@login_required
@team_required(invert=True)
@require_POST
def join_team(request: HttpRequest):
    """Create the account page."""

    form = JoinTeamForm(request.POST)

    if form.is_valid():
        team = Team.objects.get(code=form.cleaned_data['code'])
        team.user_count += 1
        team.eligible = team.eligible and request.user.userprofile.eligible

        team.save()
        team.users.add(request.user)

        request.user.userprofile.team = team
        request.user.userprofile.save()

        return reverse('account')

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': ChangePasswordForm(user=request.user),
                                            'join_team': form,
                                            'create_team': CreateTeamForm()})