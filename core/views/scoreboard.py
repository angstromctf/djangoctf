from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone

from core.models import Team, CorrectSubmission
from core.utils.time import contest_start, contest_end, minutes

def scoreboard(request: HttpRequest):
    """
    View for the scoreboard page.
    """
    team_list = Team.objects.filter(score__gt=0).order_by('-score', 'score_lastupdate')

    solutions_list = []
    graph_size = min(5, Team.objects.filter(score__gt=0).count())

    for x in range(graph_size):
        submissions = CorrectSubmission.objects.all().filter(team=team_list[x])
        
        for sub in submissions:
            delta = sub.time - contest_start

            solutions_list.append([minutes(delta)] + [-1] * x + [sub.new_score] + [-1] * (graph_size-1-x))

    delta = min(timezone.now(), contest_end) - contest_start
    solutions_list.append([minutes(delta)] + [team_list[x].score for x in range(graph_size)])
    
    solutions_list.sort()
    solutions_list.insert(0, [0] * (graph_size+1))
    solutions_list.insert(0, ['X'] + list(map(lambda x: team_list[x].name, range(graph_size))))
    solutions_list[-1] = [solutions_list[-1][0]] + list(map(lambda x: team_list[x].score, range(graph_size)))
    
    return render(request, 'scoreboard.html', {
        'user': request.user,
        'team_list': team_list,
        'data': str(solutions_list).replace('-1', 'null').replace('(', '[').replace(')', ']'),
    })