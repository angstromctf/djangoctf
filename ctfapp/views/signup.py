from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from ctfapp.forms import CreateUserForm
from ctfapp.models import User, UserProfile, ProblemSolved

import json


def signup(request):
    """
    View for the registration page.
    """
    with open('djangoctf/settings.json') as config_file:
        config = json.loads(config_file.read())
        enabled = config['registration_enabled']

    if not enabled:
        return render(request, 'signup.html', {'enabled': False})

    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {'form': CreateUserForm(), 'enabled': True})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Create our new user
            user = User.objects.create_user(form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])

            profile = UserProfile(user=user,
                                  school=form.cleaned_data['school'],
                                  eligible=form.cleaned_data['eligible'])

            if form.cleaned_data['gender']:
                profile.gender = form.cleaned_data['gender']

            if form.cleaned_data['race']:
                profile.race = form.cleaned_data['race']

            profile.save()

            # Authenticate and login our new user!
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)

            return redirect("/")
        else:
            # The form didn't validate properly
            return render(request, 'signup.html', {'form': form, 'enabled': True})