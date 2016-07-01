from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.template import Template, Context
from django.core.mail import EmailMessage
from ctfapp.models import UserProfile

from datetime import timedelta
import hashlib
import random


EXPIRATION = timedelta(days=2)

def activation(request, key):
    """
    View called from activation email. Activate user if link didn't expire (48h default)
    """
    activation_expired = False
    already_active = False
    activation_success = False
    resend_userid = ""
    profile = get_object_or_404(UserProfile, activation_key=key)

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
    return render(request, 'activation.html', {'activation_expired': activation_expired,
                                           'already_active': already_active,
                                           'activation_success': activation_success,
                                           'resend_userid': resend_userid})


def new_activation_link(request, user_id):
    data = {}
    user = User.objects.get(id=user_id)
    new_link_sent = False

    if user is not None and not user.is_active and not request.user.is_authenticated():
        data['username'] = user.username
        data['email'] = user.email

        profile = UserProfile.objects.get(user=user)
        profile.activation_key = generate_activation_key(user.username)
        profile.key_generated = timezone.now()
        profile.save()

        send_email(data, profile.activation_key, request=request)

        new_link_sent = True

    return render(request, 'activation.html', {'new_link_sent': new_link_sent})


def generate_activation_key(username):
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
    return hashlib.sha1(salt+username.encode('utf8')).hexdigest()

def send_email(data, key, request=None, use_https=False):
    sendgrid_api_key = settings.CONFIG['email']['sendgrid_api_key']
    use_https = settings.CONFIG['ssl']
    ctf_name = settings.CONFIG['ctf_name']
    ctf_domain = settings.CONFIG['ctf_platform_domain']

    current_site = get_current_site(request)
    link_protocol = 'https' if use_https else 'http'

    with open('ctfapp/templates/activation_email_template.txt', 'r') as template_file:
        template = Template(template_file.read())

    context = Context({'activation_key': key,
                       'username': data['username'],
                       'domain': current_site.domain,
                       'ctf_name': ctf_name,
                       'ctf_domain': ctf_domain,
                       'protocol': link_protocol})

    message_text = template.render(context)

    # Send an activation email through sendgrid
    message_to_field = data['email']
    email = EmailMessage('Activation Link for angstromCTF', message_text, to=[message_to_field])
    email.send()
