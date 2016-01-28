from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from ctfapp.forms import CreateUserForm
from ctfapp.models import User, UserProfile
import hashlib
import random
import json

def signup(request):
    """
    View for the registration page.
    """

    with open('djangoctf/settings.json') as config_file:
        config = json.loads(config_file.read())
        enabled = config['registration_enabled']
        emails_enabled = config['email']['enabled']

        if emails_enabled:
            sendgrid_api_key = config['email']['sendgrid_api_key']

    if not enabled:
        return render(request, 'signup.html', {'enabled': False})

    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {'form': CreateUserForm(), 'enabled': True})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            datas = {}
            datas['username'] = form.cleaned_data['username']
            datas['email'] = form.cleaned_data['email']
            datas['password'] = form.cleaned_data['password']
            datas['first_name'] = form.cleaned_data['first_name']
            datas['last_name'] = form.cleaned_data['last_name']
            datas['eligible'] = form.cleaned_data['eligible']
            datas['gender'] = form.cleaned_data['gender']
            datas['race'] = form.cleaned_data['race']
            # Generate activation key
            salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
            usernamesalt = datas['username']
            usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key'] = hashlib.sha1(salt+usernamesalt).hexdigest()




            # Authenticate and login our new user!
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            # login(request, user)

            # Send activation email
            form.sendEmail(datas)
            form.save(datas)

            email_sent_message = """An activation link was sent to the address you provided. Click the email
                                    link to activate your account."""
            # Direct user to activation email sent page
            return render(request, 'message_generic.html', {'message': email_sent_message})
        else:
            # The form didn't validate properly
            return render(request, 'signup.html', {'form': form, 'enabled': True})
