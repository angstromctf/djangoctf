from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ctfapp.models import Update

def updates(request: HttpRequest):
    """
    View for the updates page.
    """

    updates_list = Update.objects.all().order_by('time')
    return render(request, 'updates.html', {
        'user': request.user,
        'updates_list': updates_list
    })
