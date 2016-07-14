from django.shortcuts import render
from django.template.context_processors import csrf

from core.models import Problem
from core.decorators import lock_before_contest


@lock_before_contest
def problems(request):
    """Displays a list of all the problems."""

    problem_list = Problem.objects.all().order_by("value")

    # Create the context beforehand, so we can add CSRF data to it
    context = {
        "problem_list": problem_list,
        "enable_submission": request.user.is_authenticated() and request.user.profile.team
    }

    # Add CSRF protection data to the context
    context.update(csrf(request))

    return render(request, "problems.html", context)
