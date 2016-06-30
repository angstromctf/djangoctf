from django.http import HttpRequest
from django.shortcuts import render
from django.template.context_processors import csrf
from ctfapp.models import Problem
from ctfapp.decorators import lock_before_contest


@lock_before_contest
def problems(request: HttpRequest):
    """Handle a request for the problems page by retrieving and displaying a list of all the problems."""

    problem_list = Problem.objects.all().order_by("value")

    # Create the context
    context = {"user": request.user, "problem_list": problem_list, "enable_submission": False}

    if request.user.is_authenticated():
        # Load the user's solved dictionary using Pickle
        team = request.user.userprofile.team

        if team:
            context["enable_submission"] = True

    context.update(csrf(request))

    return render(request, "problems.html", context)
