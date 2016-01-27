import json
from datetime import datetime

with open('djangoctf/settings.json') as config_file:
    config = json.loads(config_file.read())

    contest = type("reference", (), {})
    contest.start = datetime.strptime(config["start_time"], "%b %d %Y %H:%M:%S")
    contest.end = datetime.strptime(config["end_time"], "%b %d %Y %H:%M:%S")

def before_start():
    return datetime.now() < contest.start

def after_end():
    return datetime.now() > contest.end

def seconds_since_start():
    delta = contest.start - datetime.now()

    return delta.days // 86400 + delta.seconds