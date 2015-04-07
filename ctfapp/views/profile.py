from django.shortcuts import render

from ctfapp.models import Problem, UserProfile

import pickle
from collections import OrderedDict

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