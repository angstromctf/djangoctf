from django.http import HttpRequest
from django.shortcuts import render_to_response

def chat(request: HttpRequest):
    """
    View for the chat page.
    """
    return render_to_response('chat.html', {
        'user': request.user,
    })