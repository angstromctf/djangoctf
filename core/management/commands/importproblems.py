from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError

from core.management import deploy
from core.models import Problem

import json
import logging
from hashlib import sha512
from os import listdir, makedirs, system, getcwd, chdir
from os.path import isdir, isfile, exists, abspath, join as join_paths
from shutil import copyfile, rmtree
from string import digits
import re

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("problems_directory", help="import problems from directory")
        parser.add_argument("-r", "--reset", help="reset all problems", action="store_true")
        parser.add_argument("-s", "--reset-static", help="reset static problem files", action="store_true")

    def handle(self, *args, **options):
        problems_path = abspath(options['problems_directory'])
        verbose = options['verbosity'] > 1

        errors = []

        static_path = join_paths(settings.PROJECT_ROOT, 'core', 'static', 'problems')

        if options['reset']:
            Problem.objects.all().delete()

        if options['reset_static']:
            rmtree(static_path)

        pattern = re.compile('\{\{([^,\}]*),([^\}]*)\}\}')

        total = 0
        successful = 0
        for category in listdir(problems_path):
            category_path = join_paths(problems_path, category)
            if not isdir(category_path) or category[0] == '.' or category[0] in digits:
                continue

            for problem in listdir(category_path):
                problem_path = join_paths(category_path, problem)
                name = category + '/' + problem

                if not isdir(problem_path):
                    self.stdout.write("Problem path not a directory for problem {:s}/{:s}".format(category, problem))
                    continue

                total += 1

                try:
                    with open(join_paths(problem_path, 'problem.json')) as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    errors.append("Failed to load metadata for problem {:s}/{:s}".format(category, problem))
                    continue

                if "enabled" in data and data["enabled"] == False:
                    total -= 1
                    continue

                data["title"] = data["name"]
                del data["name"]

                data["text"] = pattern.sub('<a href="/static/problems/' + name +
                                           '/\\1" target="_blank">\\2</a>', data["text"])
                data["hint"] = pattern.sub('<a href="/static/problems/' + name +
                                           '/\\1" target="_blank">\\2</a>', data["hint"])

                if Problem.objects.filter(name=name).exists():
                    # Update the problem if it already exists
                    try:
                        problem_obj = Problem.objects.get(name=name)
                        problem_obj.title = data["title"]
                        problem_obj.text = data["text"]
                        problem_obj.value = data["value"]
                        problem_obj.hint_text = data["hint"]
                        problem_obj.flag_sha512_hash = sha512(data["flag"].lower().encode()).hexdigest()
                        # We can't update the name for obvious reasons
                        problem_obj.save()

                        if verbose:
                            self.stdout.write("Note: Successfully updated problem {:s}".format(name))

                        successful += 1
                    except MultipleObjectsReturned:
                        errors.append("Multiple problems exist with name {:s}".format(name))
                else:
                    # Otherwise, create new problem
                    problem_obj = Problem(name=name,
                                          title=data["title"],
                                          text=data["text"],
                                          value=data["value"],
                                          category=category,
                                          hint_text=data["hint"],
                                          flag_sha512_hash=sha512(data["flag"].encode()).hexdigest())
                    problem_obj.save()

                    if verbose:
                        self.stdout.write("Note: Successfully created problem {:s}/{:s}".format(category, problem))

                    successful += 1

        self.stdout.write("Successfully imported {:d}/{:d} problems".format(successful, total))

        # Now copy static files
        # This is in a separate for loop so that static files are copied even when the problem already exists
        for category in listdir(problems_path):
            category_path = join_paths(problems_path, category)
            if not isdir(category_path) or category[0] == '.':
                continue

            for problem in listdir(category_path):
                problem_path = join_paths(category_path, problem)
                if not isdir(problem_path):
                    continue

                name = category + '/' + problem

                # Create the static path if necessary
                static_dir = join_paths(static_path, name)

                makedirs(static_dir, exist_ok=True)

                if exists(join_paths(problem_path, 'build.sh')):
                    if verbose:
                        self.stdout.write("build.sh found for {:s}, building".format(name))

                    old_path = getcwd()
                    chdir(problem_path)
                    try:
                        if system("./build.sh"):
                            errors.append("Build.sh for {:s} reported errors".format(name))
                    except NameError:
                        errors.append("Unable to build {:s}".format(name))
                    chdir(old_path)

                try:
                    with open(join_paths(problem_path, 'problem.json')) as data_file:
                        data = json.load(data_file)
                except FileNotFoundError:
                    continue

                if "deploy" in data:
                    if "enabled" not in data["deploy"] or data["deploy"]["enabled"]:
                        func = getattr(deploy, data['deploy']['script'])
                        func(data, problem, category, problem_path)

                if "files" in data:
                    for file in data["files"]:
                        file_path = join_paths(problem_path, file.strip())
                        dest = join_paths(static_dir, file.strip())

                        if len(file) == 0 or not isfile(file_path):
                            continue

                        copyfile(file_path, dest)

                        if verbose:
                            self.stdout.write("Note: Copying static file {:s} for problem {:s}".format(file.strip(), name))

        if errors:
            raise CommandError("The following error(s) occured while importing problems:\n" + "\n".join(errors) +
                               "\n{:d}/{:d} problems were imported successfully.".format(successful, total))
