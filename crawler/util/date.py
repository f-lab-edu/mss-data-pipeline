from datetime import datetime, timedelta, timezone


def subtract_date(date, day):
    return date - timedelta(days=int(day))


def KST_now():
    utc_now = datetime.now(timezone.utc)
    KST = timezone(timedelta(hours=9))
    return utc_now.astimezone(KST)
