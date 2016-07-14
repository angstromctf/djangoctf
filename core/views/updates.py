from django.shortcuts import render

from core.models import ProblemUpdate


def updates(request):
    """Handles a request for the updates page by sorting and displaying all the updates in the database."""

    updates_list = ProblemUpdate.objects.all().order_by('-time')

    return render(request, 'updates.html', {
        'updates': updates_list
    })
