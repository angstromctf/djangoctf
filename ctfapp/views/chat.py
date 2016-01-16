from django.http import HttpRequest
from django.shortcuts import render_to_response
#The chat page. Uses kiwiirc for the chat client 

# Handle the HTTP request
def chat(request: HttpRequest):
    """Create the chat page."""
    return render_to_response("chat.html", {"user": request.user})
