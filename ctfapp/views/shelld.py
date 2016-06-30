from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ctfapp.decorators import lock_before_contest


@login_required
@lock_before_contest
def shelld(request: HttpRequest):
    """Handle a request for the scoreboard page."""

    return render(request, "shelld.html")
