from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.models import Problem, ProblemUpdate, CorrectSubmission, IncorrectSubmission, Team, Profile

class Command(BaseCommand):
    help = 'Resets the CTF game for a new year.'

    def handle(self, *args, **options):
        def yesno(prompt, default=True):
            yes = ['yes', 'ye', 'y']
            no = ['no', 'n']

            answer = input(prompt + " [Y/n] ")
            while answer.lower() not in yes and answer.lower() not in no and answer != "":
                answer = input(prompt + " [Y/n] ")

            if answer == "":
                return default
            elif answer.lower() in yes:
                return True
            else:
                return False

        if yesno("Delete problems, updates, and submissions?"):
            Problem.objects.all().delete()
            ProblemUpdate.objects.all().delete()
            CorrectSubmission.objects.all().delete()
            IncorrectSubmission.objects.all().delete()

        if yesno("Delete teams?"):
            Team.objects.all().delete()

        if yesno("Delete users?", default=False):
            User.objects.all().delete()
            Profile.objects.all().delete()
