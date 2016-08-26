from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template import Template, Context
from django.core.mail import EmailMessage

from core.models import Profile

from datetime import timedelta
import hashlib
import random

EXPIRATION = timedelta(days=2)


# Generate a random activation key for a user
def generate_activation_key(username):
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
    return hashlib.sha1(salt+username.encode('utf8')).hexdigest()


def activation(request, key):
    """Activates the user's account."""

    activation_expired = False
    already_active = False
    activation_success = False
    resend_userid = ""
    profile = get_object_or_404(Profile, activation_key=key)

    if not profile.user.is_active:
        if timezone.now() - profile.key_generated > EXPIRATION:
            activation_expired = True
            id_user = profile.user.id
            resend_userid = str(id_user)
        else:
            profile.user.is_active = True
            activation_success = True
            profile.user.save()
    else:
        already_active = True

    return render(request, 'activation.html', {
        'activation_expired': activation_expired,
        'already_active': already_active,
        'activation_success': activation_success,
        'resend_userid': resend_userid
    })


def new_activation_link(request, user_id):
    """Resends an account activation link to the user."""

    user = get_object_or_404(User.objects, id=user_id)

    if user.is_active:
        return redirect('account')

    user.profile.activation_key = generate_activation_key(user.username)
    user.profile.key_generated = timezone.now()
    user.profile.save()

    send_activation_email(user, request=request)

    return render(request, 'activation.html', {'new_link_sent': True})


def send_activation_email(user, request=None, use_https=False):
    """Sends an activation email to a specific user."""

    use_https = settings.CONFIG['ssl']
    ctf_name = settings.CONFIG['ctf_name']
    ctf_domain = settings.CONFIG['ctf_platform_domain']

    current_site = get_current_site(request)
    link_protocol = 'https' if use_https else 'http'

    with open('core/templates/activation_email_template.txt', 'r') as template_file:
        template = Template(template_file.read())

    context = Context({
        'activation_key': user.profile.activation_key,
        'username': user.get_username(),
        'domain': current_site.domain,
        'ctf_name': ctf_name,
        'ctf_domain': ctf_domain,
        'protocol': link_protocol
    })

    message_text = template.render(context)

    # Send an activation email
    email = EmailMessage('Activation Link for angstromCTF', message_text, to=[user.email])
    email.send()
