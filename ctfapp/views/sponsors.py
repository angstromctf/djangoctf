from django.http import HttpRequest
from django.shortcuts import render


def sponsors(request: HttpRequest):
    """Handle a request for the sponsors page."""

    return render(request, "sponsors.html")
