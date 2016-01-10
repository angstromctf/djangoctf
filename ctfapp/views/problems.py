# Import
from django.http import HttpRequest
from django.shortcuts import render
from django.template.context_processors import csrf
from ctfapp.models import Problem
import pickle

# Handle the HTTP requst
def problems(request: HttpRequest):
    """View for the problems page.  Login is required."""

    problem_list = Problem.objects.all().order_by("problem_value")

    # Create the context
    context = {"user": request.user, "problem_list": problem_list}

    if request.user.is_authenticated():
        # Load the user's solved dictionary using Pickle
        team = request.user.userprofile.team

        if team:
            context["solved"] = pickle.loads(team.solved)

    context.update(csrf(request))

    # Render the page
    return render(request, "problems.html", context)
