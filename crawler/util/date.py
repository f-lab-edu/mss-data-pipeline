import datetime


def subtract_date(date, day):
    return date - datetime.timedelta(days=int(day))
