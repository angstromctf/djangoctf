from django.http import HttpRequest
from django.shortcuts import render_to_response

# Handle the HTTP request
def learn(request: HttpRequest):
    """Create the learn page."""

    return render_to_response("learn.html", {"user": request.user})
