from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("file", help="exported JSON file of problems from deploy.")

    def handle(self, *args, **options):
        print(options["file"])
