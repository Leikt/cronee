from .exceptions import CroneeOutOfBoundError, CroneeAliasError, CroneeValueError, CroneeRangeOrderError

Aliases = dict[str, set[int]]

TOKEN_JOKER = '*'
KEYWORD_RANGE = '..'


def parse_value(value: str,
                valid_range: set,
                aliases: Aliases = None) -> set[int]:
    """
    Parses a value and returns a set of integers within the valid range.

    :param value: A string representing the value to be parsed.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `value` argument. If no aliases are provided, this argument defaults to `None`.
    :return: a set of integers representing the parsed value.
    :raises: CroneeValueError, if the `value` argument is invalid.
    """
    if value == TOKEN_JOKER:
        return parse_joker(valid_range)

    if value.isnumeric():
        return parse_numeric(value, valid_range)

    if value.isalpha():
        return parse_alias(value, aliases)

    raise CroneeValueError(f"Invalid value '{value}'")


def parse_joker(valid_range: set) -> set[int]:
    """
    Returns the valid range, if inversion is False, raise an error if inversion is True

    :param valid_range: A set of integers representing the valid range of values.
    :return: a copy of the valid_range set.
    :raises: CroneeSyntaxError, if the `inversion` is True
    """
    return valid_range.copy()


def parse_numeric(value: str, valid_range: set[int]) -> set[int]:
    """
    Parses a numeric value and returns a set of integers within the valid range.

    :param value: A string representing the numeric value to be parsed.
    :param valid_range: A set of integers representing the valid range of values.
    :return: a set of integers representing the parsed value
    :raises: CroneeOutOfBoundError, if the `value` argument is out of the valid range
    """
    new_value = int(value)
    if new_value not in valid_range:
        raise CroneeOutOfBoundError(f"Value {value} is out of the valid range {valid_range}")
    return {new_value}


def parse_alias(value: str, aliases: Aliases) -> set[int]:
    """
    Parses an alphabetic value and returns a set of integers within the valid range based on the provided aliases.

    :param value: A string representing the alphabetic value to be parsed.
    :param aliases: A dictionary of string keys and set of integers values, representing possible aliases for the `value` argument.
    :return: a set of integers representing the parsed value
    :raises: CroneeAliasError, if the `value` argument is invalid alias.
    """
    new_values = aliases.get(value)
    if new_values is None:
        raise CroneeAliasError(f"Invalid alias {value}")
    return new_values


def parse_range(expression: str, valid_range: set[int], aliases: Aliases) -> set[int]:
    """
    Parses a range and returns a set of integers within the valid range.

    :param expression: A string representing the range to be parsed, in the form of 'start-stop' where 'start' and 'stop' are strings that can be parsed by the parse_value function.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `start` and `stop` arguments.
    :return: a set of integers representing the parsed range
    :raises: CroneeValueError, if the `start` or `stop` value of the range is not valid
    :raises: CroneeRangeOrderError, if the `start` value is greater than the `stop` value.
    """
    start_str, stop_str = expression.split(KEYWORD_RANGE)
    start_set = parse_value(start_str, valid_range, aliases)
    stop_set = parse_value(stop_str, valid_range, aliases)
    if len(start_set) != 1 or len(stop_set) != 1:
        raise CroneeValueError(f"Invalid start or stop value for the range '{expression}'")
    start = next(iter(start_set))
    stop = next(iter(stop_set))
    if start >= stop:
        raise CroneeRangeOrderError(
            f"The first value of a range must be less than than the second one. Invalid range '{expression}'")
    return {v for v in valid_range if start <= v <= stop}
