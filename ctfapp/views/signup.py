from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.utils import IntegrityError

from ctfapp.forms import CreateUserForm
from ctfapp.models import User, UserProfile, ProblemSolved

def signup(request):
    """
    View for the registration page.
    """
    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(CreateUserForm().as_p())

        if form.is_valid():
            # They're submitting their response
            # Keep a running list of errors
            errors = {}
            # Make sure no fields are empty
            for field in ['username', 'password', 'school', 'email']:
                if len(form.cleaned_data[field]) == 0:
                    errors[field + '_error'] = "You need a {:s}".format(field.capitalize())

            # Create the user
            try:
                user = User.objects.create_user(form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])

                profile = UserProfile(user=user,
                                      school=form.cleaned_data['school'])
                profile.save()

                solved = ProblemSolved(team=user)
                solved.save()

                # Authenticate and login our new user!
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
            except IntegrityError:
                # The username/email they're requesting is already in use
                errors['username_error'] = 'Username already in use'
                return render(request, 'signup.html', errors)
            return redirect("/")