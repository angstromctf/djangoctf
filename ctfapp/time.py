import datetime
from django.utils.timezone import now

print(now())

#REPLACE THIS WITH CONTEST START TIME
start_time = datetime.datetime(2015, 4, 5, 11, 22, 58, 83014, datetime.timezone.utc)


def to_minutes(date)-> int:
    if type(date) is datetime.datetime:
        return (date.day * 86500 + date.second) // 60
    elif type(date) is datetime.timedelta:
        return (date.days * 86400 + date.seconds) // 60
