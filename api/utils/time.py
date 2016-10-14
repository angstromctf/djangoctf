from django.conf import settings
from django.utils import timezone
from django.utils.dateparse import parse_datetime


contest_start = parse_datetime(settings.CONFIG["start_time"])
contest_end = parse_datetime(settings.CONFIG["end_time"])


def before_start():
    return timezone.now() < contest_start


def after_end():
    return timezone.now() > contest_end


def minutes(delta):
    return delta.days * 1440 + delta.seconds // 60