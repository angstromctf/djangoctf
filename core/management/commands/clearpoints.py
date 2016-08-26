from django.core.management.base import BaseCommand

from core.models import CorrectSubmission, Team, Problem


class Command(BaseCommand):
    help = 'Clears the solves for a specific problem and takes away points.'

    def add_arguments(self, parser):
        parser.add_argument('problem', type=str, help='name of problem to clear points for')

    def handle(self, *args, **options):
        problem = Problem.objects.get(name=args['problem'])

        for team in Team.objects.all():
            if problem in team.solved.all():
                team.solved.remove(problem)

                correct = CorrectSubmission.objects.get(team=team, problem=problem)
                for submission in CorrectSubmission.objects.filter(team=team):
                    if submission.time >= correct.time:
                        submission.new_score -= problem.value
                        submission.save()

                correct.delete()

                team.score -= problem.value
                team.save()
