from django.core.management.base import BaseCommand, CommandError

# from api.management import deploy
from api.models import Problem

import os
import json
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("problems", help="path to JSON dump of problems")

    def handle(self, *args, **options):
        path = os.path.abspath(options["problems"])
        with open(path) as file:
            problems = json.load(file)
        for problem in filter(None, problems):
            model = Problem.objects.filter(name=problem["name"]).first()
            if model:
                for field in problem:
                    if field != "name":
                        setattr(model, field, problem[field])
            else:
                model = Problem.objects.create(**problem)
            model.save()
