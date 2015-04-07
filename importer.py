from django.conf import settings
from djangoctf.settings import DATABASES, TIME_ZONE
from sys import argv
from os import listdir, makedirs
from os.path import isdir, isfile, realpath
from hashlib import sha512
from shutil import copyfile

if len(argv) != 2:
    print('Usage: {:s} problems_directory'.format(argv[0]))
    exit()
path = argv[1]

# Configure settings
settings.configure(DATABASES=DATABASES, TIME_ZONE=TIME_ZONE)
from ctfapp.models import *

STATIC = '/'.join(realpath(__file__).split('/')[:-1]) + '/ctfapp/static/problems'

for category in listdir(path):
    category_path = path + '/' + category
    if not isdir(category_path) or category[0] == '.':
        continue

    for problem in listdir(category_path):
        problem_path = category_path + '/' + problem
        if not isdir(problem_path):
            continue

        # Check if there's a special name file
        try:
            name = open(problem_path + '/name.txt').read()
        except FileNotFoundError:
            name = problem

        # Make sure the problem does not already exist
        if Problem.objects.filter(problem_title=name).exists():
            print("Note: Problem {:s}/{:s} already exists, skipping".format(category, problem))
            continue

        # Get the problem text and hint
        try:
            text = open(problem_path + '/problem.txt').read().strip()
            hint = open(problem_path + '/hint.txt').read().strip()
            value = int(open(problem_path + '/value.txt').read())
            flag = sha512(open(problem_path + '/flag.txt').read().strip().encode('utf-8')).hexdigest()
        except FileNotFoundError:
            print("Error: Failed to import problem {:s}/{:s}".format(category, problem))
            continue

        # Finally, create the problem
        problem_obj = Problem(problem_title=name,
                              problem_text=text,
                              problem_value=value,
                              problem_category=category,
                              hint_text=hint,
                              flag_sha512_hash=flag)
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
            files = open(problem_path + '/files.txt').readlines()
        except FileNotFoundError:
            continue

        for file in files:
            file_path = problem_path + '/' + file.strip()
            static_path = static_dir + '/' + file.strip()
            if len(file) == 0 or not isfile(file_path):
                continue
            copyfile(file_path, static_path)
            print("Note: Copying static file {:s} for problem {:s}/{:s}".format(file.strip(), category, problem))