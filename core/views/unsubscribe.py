from django.http import HttpRequest
from django.shortcuts import render


def unsubscribe(request):
    # This is a worthless view that I'll delete soon

    return render(request, "unsubscribe.html")
