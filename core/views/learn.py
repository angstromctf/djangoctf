from django.http import HttpRequest
from django.shortcuts import render


def learn(request: HttpRequest):
    """Handle a request for the learn page."""

    return render(request, "learn.html")
