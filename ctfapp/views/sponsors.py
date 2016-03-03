from django.http import HttpRequest
from django.shortcuts import render


def sponsors(request: HttpRequest):
    """Create the sponsors page."""

    return render(request, "sponsors.html", {"user": request.user})
