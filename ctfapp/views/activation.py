from django.shortcuts import render, get_object_or_404
from ctfapp.models import UserProfile
from datetime import datetime
from django.utils import timezone


def activation(request, key):
    """
    View called from activation email. Activate user if link didn't expire (48h default)
    """
    activation_expired = False
    already_active = False
    profil = get_object_or_404(UserProfile, activation_key=key)
    if profil.user.is_active == False:
        if timezone.now() > profil.key_expires:
            activation_expired = True #Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
            id_user = profil.user.id
        else: #Activation successful
            profil.user.is_active = True
            profil.user.save()

    #If user is already active, simply display error message
    else:
        already_active = True #Display : error message
    return render(request, 'activation.html', locals())
