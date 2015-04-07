from django.conf import settings
from djangoctf.settings import DATABASES, TIME_ZONE
from sys import argv
from os import listdir
from os.path import isdir
from hashlib import sha512

if len(argv) != 2:
    print('Usage: {:s} problems_directory'.format(argv[0]))
    exit()
path = argv[1]

# Configure settings
settings.configure(DATABASES=DATABASES, TIME_ZONE=TIME_ZONE)
from ctfapp.models import *

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
            name = open(category_path + '/name.txt')
        except FileNotFoundError:
            name = problem

        # Make sure the problem does not already exist
        if Problem.objects.filter(problem_title=name).exists():
            print("Note: Problem {:s}/{:s} already exists, skipping".format(category, problem))
            continue

        # Get the problem text and hint
        try:
            text = open(category_path + '/problem.txt').read().strip()
            hint = open(category_path + '/hint.txt').read().strip()
            value = int(open(category_path + '/value.txt').read())
            flag = sha512(open(category_path + '/flag.txt').read().strip()).hexdigest()
        except FileNotFoundError:
            print("Error: Failed to import problem {:s}/{:s}".format(category, problem))
            continue

        # Finally, create the problem
        problem = Problem(problem_title=name,
                          problem_text=text,
                          problem_value=value,
                          problem_category=category,
                          hint_text=hint,
                          flag_sha512_hash=flag)
        problem.save()