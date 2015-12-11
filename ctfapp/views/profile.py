# Import
from django.shortcuts import render
from ctfapp.models import Problem, UserProfile
import pickle
import collections

def profile(request, user):
    # Find all problems
    problems = collections.OrderedDict()
    for problem in Problem.objects.all()
        problems[problem.id] = problem
    # ... and all the problems the user has solved
    problems_solved = pickle.loads(UserProfile.objects.get(user__username=user).solved)

    # Now put all solved problems in the array
    for solved in problems_solved.items():
        try:
            annotated_problems[solved[0]] = (
                annotated_problems[solved[0]][0],
                annotated_problems[solved[0]][1],
                solved[1][0])
        except KeyError:
            pass

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