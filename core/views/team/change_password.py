from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm


@login_required
@require_POST
def change_password(request: HttpRequest):
    """
    View for changing a password.  Login is required.
    """


    form = ChangePasswordForm(request.POST, user=request.user)

    if form.is_valid():
        user = authenticate(username=request.user.get_username(), password=form.cleaned_data['password'])

        user.set_password(form.cleaned_data["new_password"])
        user.save()

        login(request, user)

    return render(request, 'account.html', {'user': request.user,
                                            'change_password': form,
                                            'join_team': JoinTeamForm(user=request.user),
                                            'create_team': CreateTeamForm()})
