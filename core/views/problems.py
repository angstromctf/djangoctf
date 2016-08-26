from django.template.context_processors import csrf
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.utils import timezone

from core.models import Problem, CorrectSubmission, IncorrectSubmission
from core.decorators import team_required, lock_before_contest, lock_after_contest

import hashlib
import json


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


@require_POST
@login_required
@team_required
@lock_before_contest
@lock_after_contest
def submit_problem(request):
    """Handles submissions for specific problems and returns JSON data indicating success status."""

    problem_id = int(request.POST.get("problem"))
    guess = request.POST.get("guess").strip().lower()

    problem = Problem.objects.get(id=problem_id)

    team = request.user.profile.team

    if problem in team.solved.all():
        # We've already solved the problem
        alert = "already_solved"

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

        alert = "correct"

        solved = True
    else:
        alert = "incorrect"

        if IncorrectSubmission.objects.filter(team=team, problem=problem, guess=guess).count() > 0:
            alert = "incorrect_tried"
        else:
            solution = IncorrectSubmission(team=team, problem=problem, guess=guess)
            solution.save()

        solved = False

    html = render(request, "problem.html", {
        'problem': problem,
        'guess': guess,
        'enable_submission': True,
        'solved': solved
    }).content

    response_data = {"html": html.decode("utf-8"), "alert": alert}
    return HttpResponse(json.dumps(response_data), content_type="application/json")