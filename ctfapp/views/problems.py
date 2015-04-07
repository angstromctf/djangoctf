from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ctfapp.forms import SubmitForm
from ctfapp.models import Problem, ProblemSolved

from datetime import datetime
from enum import IntEnum
import hashlib
import pickle

from ctfapp.utils import to_minutes

#REPLACE THIS WITH CONTEST START TIME
start_time = datetime(2015, 4, 5, 11, 22, 58, 83014)

class ProblemStatus(IntEnum):
    okay = 1
    wrong = 2
    correct = 3
    already = 4

@login_required
def problems(request: HttpRequest):
    """
    View for the problems page.  Login is required.
    """
    # The primary key of the last submission
    last_submission = -1

    # The status of the last submission (correct, failed, etc.)
    status = ProblemStatus.okay

    # Load the user's solved dictionary using Pickle
    solved = pickle.loads(request.user.userprofile.solved)

    # Check if this is the result of a form submission
    if request.method == 'POST':
        # Create a SubmitForm object corresponding to the POST fields in request
        form = SubmitForm(request.POST)

        if form.is_valid():
            guess = form.cleaned_data["flag_guess"]
            pid = form.cleaned_data["problem"]

            # The primary key of the last submission
            last_submission = pid

            problem = Problem.objects.get(id=pid)

            # Check if the submission was correct
            correct = hashlib.sha512(guess.encode()).hexdigest() == problem.flag_sha512_hash

            # The number of tries to display
            next_count = solved[pid][1] + 1 if pid in solved else 1

            if pid in solved and solved[pid][0]:
                # We'd already solved the problem
                status = ProblemStatus.already
            elif correct:
                # We have now solved the problem because the solution was correct
                solved[pid] = (True, next_count)
                status = ProblemStatus.correct

                # Update the user's score
                request.user.userprofile.score += problem.problem_value
                request.user.userprofile.score_lastupdate = datetime.now()

                # Add a new Solution object corresponding to having solved the problem
                delta = datetime.now() - start_time
                solution = ProblemSolved(team=request.user, new_score=request.user.userprofile.score, minutes=to_minutes(delta))
                solution.save()
            else:
                # We haven't solved the problem, the solution was bad
                solved[pid] = (False, next_count)
                status = ProblemStatus.wrong

            request.user.userprofile.solved = pickle.dumps(solved)
            request.user.userprofile.save()

    problem_list = Problem.objects.all().order_by('problem_value')
    return render(request, 'problems.html', {
        'user': request.user,
        'problem_list': problem_list,
        'form': SubmitForm(),
        'last': last_submission,
        'status': status,
        'solved': solved,
    })