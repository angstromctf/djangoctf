from django.http import HttpRequest
from django.shortcuts import render_to_response

def index(request: HttpRequest):
    """
    View for the index page.
    """
    return render_to_response('index.html', {
        'user': request.user,
    })