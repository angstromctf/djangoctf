from django.http import HttpRequest
from django.shortcuts import render

from core.utils.time import contest_start, contest_end


def index(request: HttpRequest):
    """Handle a request for the index page."""

    return render(request, "index.html", {
        "start": contest_start,
        "end": contest_end
    })
