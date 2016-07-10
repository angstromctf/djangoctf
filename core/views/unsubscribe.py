#The view for the about page. Displays information about angstrom and the project.

from django.http import HttpRequest
from django.shortcuts import render


# Handle the HTTP request
def unsubscribe(request: HttpRequest):

    return render(request, "unsubscribe.html", {})
