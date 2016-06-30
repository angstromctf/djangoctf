from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ctfapp.models import ProblemUpdate


def updates(request: HttpRequest):
    """Handle a request for the updates page by sorting and displaying all the updates in the database."""

    updates_list = ProblemUpdate.objects.all().order_by('-time')

    return render(request, 'updates.html', {
        'updates': updates_list
    })
