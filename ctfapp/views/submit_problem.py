import hashlib
import json

from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.utils import timezone

from ctfapp.models import Problem, CorrectSubmission, IncorrectSubmission
from ctfapp.decorators import team_required, lock_before_contest

# This file handles problem grading and the display for grading.


@require_POST
@login_required
@team_required
@lock_before_contest
def submit_problem(request: HttpRequest):
    """
    View for submitting a problem through AJAX.  Login is required.
    """

    pid = int(request.POST.get("problem"))
    guess = request.POST.get("guess").strip()

    problem = Problem.objects.get(id=pid)

    team = request.user.userprofile.team

    if problem in team.solved.all():
        # We've already solved the problem
        alert = "<strong>Hmm?</strong> You've already solved this."
        alert_class = "glyphicon glyphicon-info-sign"

        solved = True
    elif hashlib.sha512(guess.encode()).hexdigest() == problem.flag_sha512_hash:
        # We have now solved the problem because the solution was correct
        team.solved.add(problem)

        # Update the team's score
        team.score += problem.value

        if problem.update_time:
            team.score_lastupdate = timezone.now()

        team.save()

        # Add a new CorrectSubmission object corresponding to having solved the problem
        solution = CorrectSubmission(team=team, problem=problem, new_score=team.score)
        solution.save()

        alert = "<strong>Good job!</strong> You've solved " + problem.title.strip() + "! (+" + str(problem.value) + " points)"
        alert_class = "glyphicon glyphicon-ok-sign"

        solved = True
    else:
        alert = "<strong>Sorry.</strong> That was incorrect."

        if IncorrectSubmission.objects.filter(team=team, problem=problem, guess=guess).count() > 0:
            alert = "<strong>Oops!</strong> You've already tried this solution."
        else:
            solution = IncorrectSubmission(team=team, problem=problem, guess=guess)
            solution.save()

        alert_class = "glyphicon glyphicon-remove-sign"
        solved = False

    html = render(request, "problem.html", {
        'user': request.user,
        'problem': problem,
        'guess': guess,
        'enable_submission': True,
        'solved': solved
    }).content

    response_data = {"html": html.decode("utf-8"), "alert": alert, "alert_class": alert_class}
    return HttpResponse(json.dumps(response_data), content_type="application/json")
