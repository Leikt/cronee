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
        dtime = dtime + self.offset
        minute_is_valid = dtime.minute in self.minutes or len(self.other_validators[0]) > 0
        hour_is_valid = dtime.hour in self.hours or len(self.other_validators[1]) > 0
        dom_is_valid = dtime.day in self.doms or len(self.other_validators[2]) > 0
        month_is_valid = dtime.month in self.months or len(self.other_validators[3]) > 0
        dow_is_valid = dtime.isoweekday() in self.dows or len(self.other_validators[4]) > 0
        other_validation = self._validate_others(dtime)
        return minute_is_valid and hour_is_valid and dom_is_valid and month_is_valid and \
            dow_is_valid and other_validation

    def _validate_others(self, dtime: datetime) -> bool:
        return all([any(map(lambda v: v(dtime), validator_list)) for validator_list in self.other_validators])


def dow_index_validator(dtime: datetime, index: int, values: set[int]) -> bool:
    """
    Check if the day of the week and the index of the week match the values passed
    :param dtime: datetime object to check
    :param index: index of the week
    :param values: set of integers representing the valid days of the week
    :return: a boolean indicating if the day of the week and the index of the week match the values passed
    """
    return dtime.isoweekday() in values and math.ceil(dtime.day / 7) == index
