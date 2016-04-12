from ctfapp.models import CorrectSubmission, Problem, Team

def change_value(problem, new_value):
    value = problem.value

    for t in Team.objects.all():
        if problem in t.solved:
            t.score += new_value - value
            t.save()

            correct = CorrectSubmission.objects.get(team=t, problem=problem)
            for s in CorrectSubmission.objects.filter(team=t):
                if s.time >= correct.time:
                    s.new_score += new_value - value
                    s.save()

    problem.value = new_value
    problem.save()
