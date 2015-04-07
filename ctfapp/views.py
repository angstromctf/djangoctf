from django.http import HttpRequest
from django.shortcuts import redirect, render_to_response, render
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

from ctfapp.utils import to_minutes
from ctfapp.models import Problem, UserProfile, ProblemSolved
from ctfapp.forms import SubmitForm, LoginForm, CreateUserForm

import hashlib
import pickle
from datetime import datetime
from collections import OrderedDict

#REPLACE THIS WITH CONTEST START TIME
start_time = datetime(2015, 4, 5, 11, 22, 58, 83014)


def index(request: HttpRequest):
    """
    View for the index page.
    """
    return render_to_response('index.html', {
        'user': request.user,
    })


def scoreboard(request):
    """
    View for the scoreboard page.
    """
    user_list = UserProfile.objects.all().order_by('-score', 'score_lastupdate')
    
    solutions_list = []
    GRAPH_SIZE = min(5, len(UserProfile.objects.all()))
    for x in range(GRAPH_SIZE):
        minor = ProblemSolved.objects.all().filter(team=user_list[x].user)
        
        for j in minor:
            solutions_list.append([j.minutes] + [-1] * x + [j.new_score] + [-1] * (GRAPH_SIZE-1-x))
    
    solutions_list.sort()
    solutions_list.insert(0, ['X'] + list(map(lambda x: user_list[x].user.username, range(GRAPH_SIZE))))
    solutions_list[-1] = [solutions_list[-1][0]] + list(map(lambda x: user_list[x].score, range(GRAPH_SIZE)))
    
    return render(request, 'scoreboard.html', {
        'user': request.user,
        'user_list': user_list,
        'data': str(solutions_list).replace('-1', 'null').replace('(', '[').replace(')', ']'),
    })


@login_required
def problems(request):
    """
    View for the problems page.  Login is required.
    """
    # The primary key of the last submission
    last_submission = -1

    # The status of the last submission (correct, failed, etc.)
    status = ""

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
                status = "ALREADY"
            elif correct:
                # We have now solved the problem because the solution was correct
                solved[pid] = (True, next_count)
                status = "SOLVED"

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
                status = "FAILED"

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


def signup(request):
    """
    View for the registration page.
    """
    if request.method == 'GET':
        # Show our template
        return render(request, 'signup.html', {})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        print(CreateUserForm().as_p())

        if form.is_valid():
            # They're submitting their response
            # Keep a running list of errors
            errors = {}
            # Make sure no fields are empty
            for field in ['username', 'password', 'school', 'email']:
                if len(form.cleaned_data[field]) == 0:
                    errors[field + '_error'] = "You need a {:s}".format(field.capitalize())

            # Create the user
            try:
                user = User.objects.create_user(form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password'])

                profile = UserProfile(user=user,
                                      school=form.cleaned_data['school'])
                profile.save()

                solved = ProblemSolved(team=user)
                solved.save()

                # Authenticate and login our new user!
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
                login(request, user)
            except IntegrityError:
                # The username/email they're requesting is already in use
                errors['username_error'] = 'Username already in use'
                return render(request, 'signup.html', errors)
            return redirect("/")


def profile(request, user):
    # Find all problems
    problems = Problem.objects.all()
    # ... and all the problems the user has solved
    problems_solved = pickle.loads(UserProfile.objects.get(user__username=user).solved)
    # Create an array of all problems, set to unsolved
    annotated_problems = OrderedDict()
    for problem in problems:
        annotated_problems[problem.id] = (problem.problem_title, problem.problem_value, False)

    # Now put all solved problems in the array
    for solved in problems_solved.items():
        annotated_problems[solved[0]] = (
            annotated_problems[solved[0]][0],
            annotated_problems[solved[0]][1],
            solved[1][0]
        )

    # Finally, convert to a more usable data structure
    problems_list = []
    for item in annotated_problems.values():
        problems_list.append({
            'name': item[0],
            'value': item[1],
            'status': item[2]
        })
    problems_list.sort(key=lambda row: row['value'])

    return render(request, 'profile.html', {
        'user': user,
        'problems': problems_list
    })