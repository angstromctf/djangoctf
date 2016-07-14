from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm
from core.models import Profile


@login_required
def account(request):
    """Displays a management panel for the user's account."""

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })
