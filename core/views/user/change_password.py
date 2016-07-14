from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm


@login_required
@require_POST
def change_password(request):
    """Changes a user's password."""

    form = ChangePasswordForm(request.POST, user=request.user)

    if form.is_valid():
        user = authenticate(username=request.user.get_username(), password=form.cleaned_data['password'])

        user.set_password(form.cleaned_data["new_password"])
        user.save()

        login(request, user)

    return render(request, 'account.html', {
        'change_password': form,
        'join_team': JoinTeamForm(user=request.user),
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })
