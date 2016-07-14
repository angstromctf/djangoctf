from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from core.forms import CreateUserForm
from core.models import Profile
from core.views.user.activation import generate_activation_key, send_activation_email


def signup(request):
    """
    View for the registration page.
    """

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

            # Generate activation keys
            profile.activation_key = generate_activation_key(user.get_username())
            profile.key_generated = timezone.now()

            profile.save()

            # Send activation emails if emails are enabled
            if emails_enabled:
                send_activation_email(user, request=request)

            email_sent_message = """An activation link was sent to the address you provided. Click the email
                                        link to activate your account."""

            return render(request, 'message.html', {
                'message': email_sent_message
            })
    else:
        form = CreateUserForm()

    return render(request, 'signup.html', {
        'form': form,
        'enabled': True
    })
