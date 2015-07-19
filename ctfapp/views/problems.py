from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.context_processors import csrf

from ctfapp.models import Problem

import pickle

@login_required
def problems(request: HttpRequest):
    """
    View for the problems page.  Login is required.
    """

    # Load the user's solved dictionary using Pickle
    solved = pickle.loads(request.user.userprofile.solved)

    problem_list = Problem.objects.all().order_by('problem_value')

    context = {
        'user': request.user,
        'problem_list': problem_list,
        'solved': solved
    }
    context.update(csrf(request))

    return render(request, 'problems.html', context)