import json

import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from ctfapp.forms import CreateUserForm
from ctfapp.models import UserProfile
from ctfapp.views.users.activation import generate_activation_key, send_email


def signup(request):
    """
    View for the registration page.
    """

    with open('djangoctf/settings.json') as config_file:
        config = json.loads(config_file.read())
        enabled = config['registration_enabled']
        emails_enabled = config['email']['enabled']

        captcha_enabled = config['signup_captcha']['enabled']


    if not enabled:
        return render(request, 'signup.html', {'enabled': False})

    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {'form': CreateUserForm(), 'enabled': True})
    elif request.method == 'POST':
        if captcha_enabled:
            req = requests.post("https://www.google.com/recaptcha/api/siteverify", data=
                {'secret': config['signup_captcha']['secret'],
                 'response': request.POST.get('g-recaptcha-response')
                }
            )

            success = req.json()['success']

            if not success:
                return render(request, 'message_generic.html', {'message': 'reCAPTCHA verification failed, please try again.'})

        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
            user.is_active = not emails_enabled

            profile = UserProfile(user=user,
                                      eligible=form.cleaned_data['eligible'])

            if form.cleaned_data['gender']:
                profile.gender = form.cleaned_data['gender']
            if form.cleaned_data['race']:
                profile.race = form.cleaned_data['race']
            if form.cleaned_data['age']:
                profile.age = form.cleaned_data['age']

            user.userprofile = profile

            profile.activation_key = generate_activation_key(user.get_username())
            profile.key_generated = timezone.now()

            user.save()
            profile.save()

            if emails_enabled:
                send_email(form.cleaned_data, profile.activation_key, request=request)

            email_sent_message = """An activation link was sent to the address you provided. Click the email
                                        link to activate your account."""
            # Direct user to activation email sent page
            return render(request, 'message_generic.html', {'message': email_sent_message})
        else:
            # The form didn't validate properly
            return render(request, 'signup.html', {'form': form, 'enabled': True})
