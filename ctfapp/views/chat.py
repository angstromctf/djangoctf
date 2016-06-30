from django.http import HttpRequest
from django.shortcuts import render


def chat(request: HttpRequest):
    """Handle a request for the chat page, which uses the KiwiIRC client."""

    return render(request, "chat.html")
