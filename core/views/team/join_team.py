from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from core.models import Team
from core.decorators import team_required


@login_required
@team_required(invert=True)
@require_POST
def join_team(request):
    """Adds the user to a pre-existing team."""

    form = JoinTeamForm(request.POST)

    if form.is_valid():
        team = Team.objects.get(code=form.cleaned_data['code'])
        team.user_count += 1
        team.eligible = team.eligible and request.user.profile.eligible

        team.save()
        team.users.add(request.user)

        request.user.profile.team = team
        request.user.profile.save()

        return redirect('account')

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': form,
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })