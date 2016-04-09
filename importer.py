from django import setup
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from djangoctf.settings import DATABASES, TIME_ZONE, INSTALLED_APPS

from os import listdir, makedirs, system, getcwd, chdir
from os.path import isdir, isfile, realpath, exists
from hashlib import sha512
from shutil import copyfile, rmtree
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("problems_directory", help="import problems from directory")
parser.add_argument("-r", "--reset", help="reset all problems", action="store_true")
parser.add_argument("-s", "--reset-static", help="reset static problem files", action="store_true")
parser.add_argument("-v", "--verbose", help="show successful imports (not just errors)", action="store_true")

args = parser.parse_args()

path = args.problems_directory

# Configure settings
settings.configure(DATABASES=DATABASES, TIME_ZONE=TIME_ZONE, INSTALLED_APPS=INSTALLED_APPS)
setup()

from ctfapp.models import *

STATIC = '/'.join(realpath(__file__).replace('\\', '/').split('/')[:-1]) + '/ctfapp/static/problems'

if args.reset:
    Problem.objects.all().delete()

if args.reset_static:
    rmtree(STATIC)

pattern = re.compile('\{\{([^,\}]*),([^\}]*)\}\}')

for category in listdir(path):
    category_path = path + '/' + category
    if not isdir(category_path) or category[0] == '.':
        continue

    for problem in listdir(category_path):
        problem_path = category_path + '/' + problem
        name = category + '/' + problem

        if not isdir(problem_path):
            continue

        try:
            with open(problem_path + '/problem.json') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            print("Error: Failed to import problem {:s}/{:s}".format(category, problem))
            continue

        if "enabled" in data and data["enabled"] == False:
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
                problem_obj.flag_sha512_hash = sha512(data["flag"].encode()).hexdigest()
                # We can't update the name for obvious reasons
                problem_obj.save()

                if args.verbose:
                    print("Note: Successfully updated problem {:s}".format(name))
            except MultipleObjectsReturned:
                print("Error: Multiple problems exist with name {:s}".format(name))
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

            if args.verbose:
                print("Note: Successfully created problem {:s}/{:s}".format(category, problem))

print()
# Now copy static files
# This is in a seperate for loop so that static files are copied even when their respective problem already exists
for category in listdir(path):
    category_path = path + '/' + category
    if not isdir(category_path) or category[0] == '.':
        continue

    for problem in listdir(category_path):
        problem_path = category_path + '/' + problem
        if not isdir(problem_path):
            continue

        name = category + '/' + problem

        # Create the static path if necessary
        static_dir = STATIC + '/' + name

        makedirs(static_dir, exist_ok=True)

        if exists(problem_path + '/build.sh'):
            if args.verbose:
                print("build.sh found for {:s}, building".format(name))

            oldpath = getcwd()
            chdir(problem_path)
            try:
                if system("./build.sh"):
                    print("Build.sh for {:s} reported errors".format(name))
            except NameError:
                print("Unable to build {:s}".format(name))
            chdir(oldpath)

        try:
            with open(problem_path + '/problem.json') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            continue

        if "files" in data:
            for file in data["files"]:
                file_path = problem_path + '/' + file.strip()
                static_path = static_dir + '/' + file.strip()
                if len(file) == 0 or not isfile(file_path):
                    continue
                copyfile(file_path, static_path)

                if args.verbose:
                    print("Note: Copying static file {:s} for problem {:s}".format(file.strip(), name))
