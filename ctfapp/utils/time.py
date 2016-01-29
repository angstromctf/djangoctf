from django.utils.timezone import now, is_aware
from django.utils.dateparse import parse_datetime

import json

with open('djangoctf/settings.json') as config_file:
    config = json.loads(config_file.read())

    contest_start = parse_datetime(config["start_time"])
    contest_end = parse_datetime(config["end_time"])

def before_start():
    return now() < contest_start

def after_end():
    return now() > contest_end

def minutes(delta):
    return delta.days * 1440 + delta.seconds // 60