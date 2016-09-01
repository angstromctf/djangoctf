from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils import timezone

from core.forms import ChangePasswordForm, CreateTeamForm, JoinTeamForm, TeamAddressForm, CreateUserForm
from core.models import Profile
from core.views.activation import generate_activation_key, send_activation_email


@login_required
def account(request):
    """Displays a management panel for the user's account."""

    return render(request, 'account.html', {
        'change_password': ChangePasswordForm(user=request.user),
        'join_team': JoinTeamForm(user=request.user),
        'create_team': CreateTeamForm(),
        'address_form': TeamAddressForm()
    })


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


@login_required
def score(request):
    """Displays the score in the menu bar. Reloaded when the player solves a problem."""

    return render(request, "score.html")


def signup(request):
    """Lets the user sign up for an account."""

    enabled = settings.CONFIG['registration_enabled']
    emails_enabled = settings.CONFIG['email']['enabled']

    if not enabled:
        return render(request, 'signup.html', {
            'enabled': False
        })

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # Create user
            user = User.objects.create_user(form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'],
                                            first_name=form.cleaned_data['first_name'],
                                            last_name=form.cleaned_data['last_name'])
            user.is_active = not emails_enabled

            user.save()

            # Create user profile
            profile = Profile(user=user,
                              eligible=form.cleaned_data['eligible'])

            # Add in optional demographics data
            if form.cleaned_data['gender']:
                profile.gender = form.cleaned_data['gender']
            if form.cleaned_data['race']:
                profile.race = form.cleaned_data['race']
            if form.cleaned_data['age']:
                profile.age = form.cleaned_data['age']
            #if form.cleaned_data['country']:
            #    profile.age = form.cleaned_data['country']

            # Generate activation keys
            profile.activation_key = generate_activation_key(user.get_username())
            profile.key_generated = timezone.now()

            profile.save()

            if emails_enabled:
                # Send activation emails if emails are enabled
                send_activation_email(user, request=request)

                email_sent_message = """An activation link was sent to the address you provided. Click the email
                                            link to activate your account."""

                return render(request, 'message.html', {
                    'message': email_sent_message
                })
            else:
                # Just log the user in
                user = authenticate(username=user.get_username(), password=form.cleaned_data['password'])
                print(user)

                login(request, user)

                return redirect('index')
    else:
        form = CreateUserForm()

    return render(request, 'signup.html', {
        'form': form,
        'enabled': True
    })
