from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from ctfapp.forms import CreateUserForm
from ctfapp.models import User, UserProfile, ProblemSolved

import configparser


def signup(request):
    """
    View for the registration page.
    """
    parser = configparser.ConfigParser()
    parser.read('../../djangoctf/secure.ini')

    enabled = parser['secret'].getboolean('SignupEnabled')

    if not enabled:
        return render(request, 'signup.html', {'enabled': False})

    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {'form': CreateUserForm(), 'enabled': True})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Create our new user
            user = User.objects.create_user(form.cleaned_data['teamname'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])

            profile = UserProfile(user=user,
                                  school=form.cleaned_data['school'])
            profile.save()

            solved = ProblemSolved(team=user)
            solved.save()

            # Authenticate and login our new user!
            user = authenticate(username=form.cleaned_data['teamname'], password=form.cleaned_data['password'])
            login(request, user)

            return redirect("/")
        else:
            # The form didn't validate properly
            return render(request, 'signup.html', {'form': form, 'enabled': True})