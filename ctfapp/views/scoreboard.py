from django.http import HttpRequest
from django.shortcuts import render
from django.utils.timezone import now

from ctfapp.models import Team, CorrectSubmission
from ctfapp.utils.time import contest_start

def scoreboard(request: HttpRequest):
    """
    View for the scoreboard page.
    """
    team_list = Team.objects.all().order_by('-score', 'score_lastupdate')
    
    solutions_list = []
    GRAPH_SIZE = min(5, len(Team.objects.all()))
    for x in range(GRAPH_SIZE):
        submissions = CorrectSubmission.objects.all().filter(team=team_list[x])
        
        for sub in submissions:
            delta = sub.time - contest_start

            solutions_list.append([delta.days * 1440 + delta.seconds // 60] + [-1] * x + [sub.new_score] + [-1] * (GRAPH_SIZE-1-x))

        solutions_list.append([])
    
    solutions_list.sort()
    solutions_list.insert(0, [0] * (GRAPH_SIZE+1))
    solutions_list.insert(0, ['X'] + list(map(lambda x: team_list[x].name, range(GRAPH_SIZE))))
    solutions_list[-1] = [solutions_list[-1][0]] + list(map(lambda x: team_list[x].score, range(GRAPH_SIZE)))

    print(solutions_list)
    
    return render(request, 'scoreboard.html', {
        'user': request.user,
        'team_list': team_list,
        'data': str(solutions_list).replace('-1', 'null').replace('(', '[').replace(')', ']'),
    })