from django.core.management.base import BaseCommand

from api.models import Submission, Team


class Command(BaseCommand):
    help = 'Recalculates all team scores in event of scoring error based on CorrectSubmission objects.'

    def handle(self, *args, **options):

        for i, team in enumerate(Team.current().all()):
            score = 0

            team.solved.clear()

            for submission in Submission.objects.all().filter(team=team).order_by('time'):
                score += submission.problem.value
                submission.new_score = score
                submission.save()
                team.solved.add(submission.problem)

            team.score = score
            team.save()

            print("Fixed score for team {%d}/{%d}" % (i, Team.objects.count()))
