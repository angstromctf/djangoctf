from datetime import datetime
import hashlib
import pickle
import json

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from ctfapp.models import Problem, ProblemSolved
from ctfapp.util.time import to_minutes, start_time


@login_required
def submit_problem(request: HttpRequest):
    """
    View for submitting a problem through AJAX.  Login is required.
    """

    # Load the user's solved dictionary using Pickle
    solved = pickle.loads(request.user.userprofile.team.solved)

    if request.method == "POST":
        pid = int(request.POST.get("problem"))
        guess = request.POST.get("guess").strip()

        problem = Problem.objects.get(id=pid)

        # Check if the submission was correct
        guess_hash = hashlib.sha512(guess.encode()).hexdigest()
        correct = guess_hash == problem.flag_sha512_hash

        # The number of tries to display
        next_count = solved[pid][1] + 1 if pid in solved else 1
        next_tries = list(set(solved[pid][2] + [guess_hash])) if pid in solved else [guess_hash]

        if pid in solved and solved[pid][0]:
            # We've already solved the problem
            alert = "<strong>Hmm?</strong> You've already solved this."
            alert_type = "info"
            alert_class = "glyphicon glyphicon-info-sign"
        elif correct:
            # We have now solved the problem because the solution was correct
            solved[pid] = (True, next_count, next_tries)

            # Update the user's score
            request.user.userprofile.team.score += problem.problem_value
            request.user.userprofile.team.score_lastupdate = datetime.now()

            # Add a new Solution object corresponding to having solved the problem
            delta = timezone.now() - start_time
            solution = ProblemSolved(team=request.user.userprofile.team, new_score=request.user.userprofile.team.score, minutes=to_minutes(delta))
            solution.save()

            alert = "<strong>Good job!</strong> You've solved " + problem.problem_title.strip() + "! (+" + str(problem.problem_value) + " points)"
            alert_type = "success"
            alert_class = "glyphicon glyphicon-ok-sign"
        else:
            alert = "<strong>Sorry.</strong> That was incorrect."

            if pid in solved and guess_hash in solved[pid][2]:
                alert = "<strong>Oops!</strong> You've already tried this solution."

            alert_type = "danger"
            alert_class = "glyphicon glyphicon-remove-sign"

            # We haven't solved the problem, the solution was bad
            solved[pid] = (False, next_count, next_tries)

        request.user.userprofile.team.solved = pickle.dumps(solved)
        request.user.userprofile.team.save()

        html = render(request, "problem.html", {
            'user': request.user,
            'problem': problem,
            'solved': solved,
            'guess': guess,
            'answer': True
        }).content

        response_data = {"html": html.decode("utf-8"), "alert": alert, "alert_type": alert_type, "alert_class": alert_class}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse("Must be POST.")
