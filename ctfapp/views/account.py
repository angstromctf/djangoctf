from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from ctfapp.forms import ChangePasswordForm

# Handle the HTTP request
@login_required
def account(request: HttpRequest):
    """Create the account page."""

    rendering_args = {'change_password': ChangePasswordForm(), 'user': request.user}

    if request.method == 'POST':
        change_password = ChangePasswordForm(request.POST)

        if change_password.is_valid():
            #Authenticate the user
            user = authenticate(username=request.user.get_username(), password=change_password.cleaned_data['password'])
            user.set_password(change_password.cleaned_data['new_password'])

        else:
            # The form didn't validate properly
            rendering_args['change_password'] = change_password

    return render(request, 'account.html', rendering_args)
