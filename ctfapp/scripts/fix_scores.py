from ctfapp.models import CorrectSubmission, Problem, Team

def fix_scores():
    for t in Team.objects.all():
        score = 0

        for s in CorrectSubmission.objects.all().order_by('time'):
            score += s.problem.value
            s.new_score = score
            s.save()

        t.score = score
        t.save()