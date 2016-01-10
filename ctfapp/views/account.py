from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ctfapp.forms import ChangePasswordForm

# Handle the HTTP request
@login_required
def account(request: HttpRequest):
    """Create the account page."""

    return render(request, 'account.html', {'change_password': ChangePasswordForm(),
                                            'user': request.user})
