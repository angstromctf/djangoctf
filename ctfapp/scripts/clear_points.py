from ctfapp.models import CorrectSubmission, Team

def clear_points(problem):
    for t in Team.objects.all():
        if problem in t.solved.all():

            correct = CorrectSubmission.objects.get(team=t, problem=problem)
            for s in CorrectSubmission.objects.filter(team=t):
                if s.time >= correct.time:
                    s.new_socore -= problem.value
                    s.save()

            correct.delete()

        t.score -= problem.value
        t.save()
