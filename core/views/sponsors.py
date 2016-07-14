from django.http import HttpRequest
from django.shortcuts import render


def sponsors(request: HttpRequest):
    """Displays the competition sponsors."""

    return render(request, "sponsors.html")
