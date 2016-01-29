from django.shortcuts import render
from ctfapp.views.activation import generate_activation_key
from ctfapp.forms import CreateUserForm
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
            datas['activation_key'] = generate_activation_key(datas['username'])

            # Send activation email
            form.sendEmail(datas, request)
            form.save(datas)

            email_sent_message = """An activation link was sent to the address you provided. Click the email
                                    link to activate your account."""
            # Direct user to activation email sent page
            return render(request, 'message_generic.html', {'message': email_sent_message})
        else:
            # The form didn't validate properly
            return render(request, 'signup.html', {'form': form, 'enabled': True})
