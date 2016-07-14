from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def score(request: HttpRequest):
    """Displays the score in the menu bar. Reloaded when the player solves a problem."""

    return render(request, "score.html")
