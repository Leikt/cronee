from datetime import datetime


def easy_datetime(
        year: int = None,
        month: int = None,
        day: int = None,
        hour: int = None,
        minute: int = None) -> datetime:
    now = datetime.now()
    return datetime(
        year=2023 if year is None else year,
        month=now.month if month is None else month,
        day=now.day if day is None else day,
        hour=now.hour if hour is None else hour,
        minute=now.minute if minute is None else minute
    )
