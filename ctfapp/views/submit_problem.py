from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ctfapp.models import Problem, ProblemSolved

from datetime import datetime
import hashlib
import pickle

import json

from ctfapp.time import to_minutes, start_time

@login_required
def submit_problem(request: HttpRequest):
    """
    View for submitting a problem through AJAX.  Login is required.
    """

    # Load the user's solved dictionary using Pickle
    solved = pickle.loads(request.user.userprofile.solved)
    alert = ""

    if request.method == "POST":
        pid = int(request.POST.get("problem"))
        guess = request.POST.get("guess")

        problem = Problem.objects.get(id=pid)

        # Check if the submission was correct
        correct = hashlib.sha512(guess.encode()).hexdigest() == problem.flag_sha512_hash

        # The number of tries to display
        next_count = solved[pid][1] + 1 if pid in solved else 1

        if pid in solved and solved[pid][0]:
            # We've already solved the problem
            alert = "<strong>Hmm?</strong> You've already solved this."
            alert_type = "info"
            alert_class = "glyphicon glyphicon-info-sign"
        elif correct:
            # We have now solved the problem because the solution was correct
            solved[pid] = (True, next_count)

            # Update the user's score
            request.user.userprofile.score += problem.problem_value
            request.user.userprofile.score_lastupdate = datetime.now()

            # Add a new Solution object corresponding to having solved the problem
            delta = timezone.now() - start_time
            solution = ProblemSolved(team=request.user, new_score=request.user.userprofile.score, minutes=to_minutes(delta))
            solution.save()

            alert = "<strong>Good job!</strong> You've solved " + problem.problem_title.strip() + "! (+" + str(problem.problem_value) + " points)"
            alert_type = "success"
            alert_class = "glyphicon glyphicon-ok-sign"
        else:
            # We haven't solved the problem, the solution was bad
            solved[pid] = (False, next_count)

            alert = "<strong>Sorry.</strong> That was incorrect."
            alert_type = "danger"
            alert_class = "glyphicon glyphicon-remove-sign"

        request.user.userprofile.solved = pickle.dumps(solved)
        request.user.userprofile.save()

    html = render(request, "problem.html", {
        'user': request.user,
        'problem': problem,
        'solved': solved
    }).content

    response_data = {"html": html.decode("utf-8"), "alert": alert, "alert_type": alert_type, "alert_class": alert_class}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


