from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Protocol


class Cronee(Protocol):
    """Class describing a Cron Extended Expression. It can validate a date and forecast the next valid datetime."""

    def validate(self, dtime: datetime) -> bool:
        """Check if the given datetime validates the cronee"""


@dataclass
class SimpleCronee:
    """Manage a simple cronee"""

    minutes: set[int]
    hours: set[int]
    doms: set[int]
    months: set[int]
    dows: set[int]
    offset: timedelta

    def validate(self, dtime: datetime) -> bool:
        dtime = dtime + self.offset
        minute_is_valid = dtime.minute in self.minutes
        hour_is_valid = dtime.hour in self.hours
        dom_is_valid = dtime.day in self.doms
        month_is_valid = dtime.month in self.months
        dow_is_valid = dtime.isoweekday() in self.dows
        return minute_is_valid and hour_is_valid and dom_is_valid and month_is_valid and dow_is_valid
