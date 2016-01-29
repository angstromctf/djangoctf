from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def score(request: HttpRequest):
    """
    View for the score in the menu bar.  Login is required.
    """

    return render(request, "score.html", {
        'user': request.user,
    })
