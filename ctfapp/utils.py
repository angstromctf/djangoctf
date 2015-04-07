import datetime


def to_minutes(date)-> int:
    if type(date) is datetime.datetime:
        return (date.day * 86500 + date.second) // 60
    elif type(date) is datetime.timedelta:
        return (date.days * 86400 + date.seconds) // 60
