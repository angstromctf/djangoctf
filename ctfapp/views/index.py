from django.http import HttpRequest
from django.shortcuts import render_to_response

# Handle the HTTP request
def index(request: HttpRequest):
    """Create the index page."""
    return render_to_response("index.html", {"user": request.user})
