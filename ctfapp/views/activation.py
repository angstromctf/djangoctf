from django.shortcuts import render, get_object_or_404
from ctfapp.models import UserProfile
from ctfapp.forms import CreateUserForm
from django.contrib.auth.models import User
import hashlib
import random
from django.utils import timezone
from datetime import datetime, timedelta


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
        if timezone.now() > profile.key_expires:
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
    form = CreateUserForm()
    datas = {}
    user = User.objects.get(id=user_id)
    new_link_sent = False
    if user is not None and not user.is_active and not request.user.is_authenticated():
        datas['username'] = user.username
        datas['email'] = user.email
        datas['activation_key'] = generate_activation_key(datas['username'])
        profile = UserProfile.objects.get(user=user)
        profile.activation_key = datas['activation_key']
        expire_date = datetime.now() + timedelta(days=2)
        profile.key_expires = datetime.strftime(expire_date, "%Y-%m-%d %H:%M:%S")
        profile.save()
        form.sendEmail(datas, request)
        request.session['new_link'] = True
        new_link_sent = True
    return render(request, 'activation.html', {'new_link_sent': new_link_sent})


def generate_activation_key(username):
    salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:5].encode('utf8')
    return hashlib.sha1(salt+username.encode('utf8')).hexdigest()
