from django.http import HttpRequest
from django.shortcuts import render_to_response


# Handle the HTTP request
def rules(request: HttpRequest):
    """Create the rules page."""

    return render_to_response("rules.html", {"user": request.user})
