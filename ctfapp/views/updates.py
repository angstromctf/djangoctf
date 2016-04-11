from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ctfapp.models import ProblemUpdate


def updates(request: HttpRequest):
    """
    View for the updates page.
    """

    updates_list = ProblemUpdate.objects.all().order_by('-time')

    return render(request, 'updates.html', {
        'user': request.user,
        'updates': updates_list
    })
