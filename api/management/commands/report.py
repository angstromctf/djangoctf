from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Sum, Avg, Count


from api.models import User, Team, Problem, Submission


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("""
        ===================================================
        Total users: {}
        Total teams: {}
        Users/team: {}
        Eligible teams: {}
        
        Total problems: {}
        Total submissions: {}
        Scoring teams: {}
        
        Countries: {}
        States: {}
        ===================================================
        """.format(User.objects.count(),
                    Team.current().count(),
                    Team.current().annotate(count=Count("members")).aggregate(Avg("count"))['count__avg'],
                    Team.current().filter(eligible=True).count(),

                    Problem.current().count(),
                    Problem.current().annotate(count=Count("solves")).aggregate(Sum("count"))['count__sum'],
                    Team.current().filter(score__gt=0).count(),

                    Team.current().filter(score__gt=0).values("members__profile__country").distinct().count(),
                    Team.current().filter(score__gt=0).values("members__profile__state").distinct().count()
                    ))