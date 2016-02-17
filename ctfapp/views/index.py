from django.http import HttpRequest
from django.shortcuts import render


def index(request: HttpRequest):
    """Create the index page."""

    return render(request, "index.html", {"user": request.user})
