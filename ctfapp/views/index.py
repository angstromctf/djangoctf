from django.http import HttpRequest
from django.shortcuts import render

from ctfapp.utils.time import contest_start, contest_end


def index(request: HttpRequest):
    """Create the index page.
    :param request: the HTTP Request
    """

    return render(request, "index.html", {"user": request.user, "start": contest_start, "end": contest_end})
