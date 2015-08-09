from django import setup
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from djangoctf.settings import DATABASES, TIME_ZONE

from os import listdir, makedirs
from os.path import isdir, isfile, realpath
from hashlib import sha512
from shutil import copyfile, rmtree
import argparse
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument("problems_directory", help="import problems from directory")
parser.add_argument("-r", "--reset", help="reset all problems", action="store_true")
parser.add_argument("-s", "--reset-static", help="reset static problem files", action="store_true")

args = parser.parse_args()

path = args.problems_directory

# Configure settings
settings.configure(DATABASES=DATABASES, TIME_ZONE=TIME_ZONE)
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
        if not isdir(problem_path):
            continue

        try:
            with open(problem_path + '/problem.json') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            print("Error: Failed to import problem {:s}/{:s}".format(category, problem))
            continue

        data["text"] = pattern.sub("<a href=\"/static/problems/" + category + "/" + problem +
                                   "/\\1\" target=\"_blank\">\\2</a>", data["text"])
        data["hint"] = pattern.sub("<a href=\"/static/problems/" + category + "/" + problem +
                                   "/\\1\" target=\"_blank\">\\2</a>", data["hint"])

        if Problem.objects.filter(problem_title=data["name"]).exists():
            # Update the problem if it already exists
            try:
                problem_obj = Problem.objects.get(problem_title=data["name"])
                problem_obj.problem_text = data["text"]
                problem_obj.hint_text = data["hint"]
                problem_obj.problem_value = data["value"]
                problem_obj.flag_sha512_hash = sha512(data["flag"].encode()).hexdigest()
                # We can't update the name for obvious reasons
                problem_obj.save()

            except MultipleObjectsReturned:
                print("Error: Multiple problems exist with name {:s}".format(data["name"]))
                continue
            print("Note: Successfully updated problem {:s}/{:s}".format(category, problem))
        else:
            # Otherwise, create new problem
            problem_obj = Problem(problem_title=data["name"],
                                  problem_text=data["text"],
                                  problem_value=data["value"],
                                  problem_category=category,
                                  hint_text=data["hint"],
                                  flag_sha512_hash=sha512(data["flag"].encode()).hexdigest())
            problem_obj.save()
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

        # Create the static path if necessary
        static_dir = STATIC + '/' + category + '/' + problem

        makedirs(static_dir, exist_ok=True)

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
                print("Note: Copying static file {:s} for problem {:s}/{:s}".format(file.strip(), category, problem))