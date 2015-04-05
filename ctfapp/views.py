from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from .models import Problem, UserProfile
from .forms import SubmitForm, LoginForm

import hashlib
import pickle
from datetime import datetime


def index(request):
    return render_to_response('index.html', {
        'user': request.user,
    })


def scoreboard(request):
    user_list = UserProfile.objects.all().order_by('-score', 'score_lastupdate')
    return render(request, 'scoreboard.html', {
        'user': request.user,
        'user_list': user_list,
    })


@login_required
def problems(request):
    last_submission = -1
    status = ""

    solved = pickle.loads(request.user.userprofile.solved)

    if request.method == 'POST':
        form = SubmitForm(request.POST)

        if form.is_valid():
            guess = form.cleaned_data["flag_guess"]
            pid = form.cleaned_data["problem"]
            last_submission = pid

            problem = Problem.objects.get(id=pid)
            good = hashlib.sha512(guess.encode()).hexdigest() == problem.flag_sha512_hash

            next_count = solved[pid][1] + 1 if pid in solved else 1
            if pid in solved and solved[pid][0]:
                status = "ALREADY"
            elif good:
                solved[pid] = (True, next_count)
                request.user.userprofile.score += problem.problem_value
                request.user.userprofile.score_lastupdate = datetime.now()
                status = "SOLVED"
            else:
                solved[pid] = (False, next_count)
                status = "FAILED"

            request.user.userprofile.solved = pickle.dumps(solved)
            request.user.userprofile.save()

    problem_list = Problem.objects.all()
    return render(request, 'problems.html', {
        'user': request.user,
        'problem_list': problem_list,
        'form': SubmitForm(),
        'last': last_submission,
        'status': status,
        'solved': solved,
    })


def signup(request):
    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {})
    elif request.method == 'POST':
        # They're submitting their response
        # Keep a running list of errors
        errors = {}
        # Make sure no fields are empty
        for field in ['username', 'password', 'school', 'email']:
            if len(request.POST[field]) == 0:
                errors[field + '_error'] = "You need a {:s}".format(field.capitalize())
        # Create the user
        try:
            user = User.objects.create_user(request.POST['username'],
                                            request.POST['email'],
                                            request.POST['password'])
            profile = UserProfile(user=user,
                                  school=request.POST['school'])
            profile.save()
        except IntegrityError as e:
            # The username/email they're requesting is already in use
            errors['username_error'] = 'Username already in use'
            return render(request, 'signup.html', errors)
        return redirect("/")