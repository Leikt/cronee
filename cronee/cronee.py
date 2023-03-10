import math
from dataclasses import dataclass
from datetime import timedelta, datetime
from typing import Protocol, Callable

Validator = Callable[[datetime], bool]
IndexValidator = Callable[[datetime, int, set[int]], bool]


class Cronee(Protocol):
    """Class describing a Cron Extended Expression. It can validate a date and forecast the next valid datetime."""

    def validate(self, dtime: datetime) -> bool:
        """Check if the given datetime validates the cronee"""

    def next_occurrence(self, start: datetime = None) -> datetime:
        """Compute the next datetime when the expression is validated starting at the start parameter"""

    def next_occurrences(self, dtime: datetime, count: int = 10) -> list[datetime]:
        """Compute the next occurrences."""


@dataclass
class SimpleCronee:
    """Manage a simple cronee"""

    minutes: set[int]
    hours: set[int]
    doms: set[int]
    months: set[int]
    dows: set[int]
    offset: timedelta
    other_validators: list[list[Validator]]

    def validate(self, dtime: datetime) -> bool:
        """ Check if the datetime is valid """
        dtime = dtime + self.offset
        minute_is_valid = dtime.minute in self.minutes or self._dynamic_validation(0, dtime)
        hour_is_valid = dtime.hour in self.hours or self._dynamic_validation(1, dtime)
        dom_is_valid = dtime.day in self.doms or self._dynamic_validation(2, dtime)
        month_is_valid = dtime.month in self.months or self._dynamic_validation(3, dtime)
        dow_is_valid = dtime.isoweekday() in self.dows or self._dynamic_validation(4, dtime)
        return minute_is_valid and hour_is_valid and dom_is_valid and month_is_valid and dow_is_valid

    def _dynamic_validation(self, index: int, dtime: datetime) -> bool:
        return any(map(lambda v: v(dtime), self.other_validators[index]))

    def next_occurrence(self, dtime: datetime) -> datetime:
        delta = timedelta(minutes=1)
        while not self.validate(dtime):
            dtime += delta
        return dtime

    def next_occurrences(self, dtime: datetime, count: int = 10) -> list[datetime]:
        delta = timedelta(minutes=1)
        occurrences = []
        for i in range(count):
            dtime = self.next_occurrence(dtime)
            occurrences.append(dtime)
            dtime = dtime + delta
        return occurrences


def dow_index_validator(dtime: datetime, index: int, values: set[int]) -> bool:
    """
    Check if the day of the week and the index of the week match the values passed
    :param dtime: datetime object to check
    :param index: index of the week
    :param values: set of integers representing the valid days of the week
    :return: a boolean indicating if the day of the week and the index of the week match the values passed
    """
    return dtime.isoweekday() in values and math.ceil(dtime.day / 7) == index
