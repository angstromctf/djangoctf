from django.core.management.base import BaseCommand

# from api.management import deploy
from api.models import Team


class Command(BaseCommand):

    def handle(self, *args, **options):
        for team in Team.objects.all():
            print(team.shell_username + " " + team.shell_password)
