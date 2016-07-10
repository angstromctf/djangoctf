from core.models import CorrectSubmission, Problem, Team

def fix_scores():
    i = 0

    for t in Team.objects.all():
        score = 0

        t.solved
        t.clear()

        for s in CorrectSubmission.objects.all().filter(team=t).order_by('time'):
            score += s.problem.value
            s.new_score = score
            s.save()
            t.solved.add(s.problem)

        t.score = score
        t.save()

        i += 1
        print("Fixed score for team {%d}/{%d}" % (i, Team.objects.count()))