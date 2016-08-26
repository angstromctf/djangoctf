from django.core.management.base import BaseCommand

from core.models import CorrectSubmission, Team


class Command(BaseCommand):
    help = 'Recalculates all team scores in event of scoring error based on CorrectSubmission objects.'

    def handle(self, *args, **options):
        i = 0

        for team in Team.objects.all():
            score = 0

            team.solved
            team.clear()

            for submission in CorrectSubmission.objects.all().filter(team=team).order_by('time'):
                score += submission.problem.value
                submission.new_score = score
                submission.save()
                team.solved.add(submission.problem)

            team.score = score
            team.save()

            i += 1
            print("Fixed score for team {%d}/{%d}" % (i, Team.objects.count()))