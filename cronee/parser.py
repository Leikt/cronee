import shlex
from datetime import timedelta
from functools import partial
from typing import Callable, Optional

from .exceptions import CroneeOutOfBoundError, CroneeAliasError, CroneeValueError, CroneeRangeOrderError, \
    CroneeSyntaxError, CroneeEmptyValuesError
from .cronee import IndexValidator, Validator, dow_index_validator, Cronee, SimpleCronee

Aliases = dict[str, set[int]]
ElementParser = Callable[[str, set[int], Aliases], tuple[Optional[Validator], set[int]]]

TOKEN_JOKER = '*'
KEYWORD_RANGE = '..'
KEYWORD_STEP = '/'
KEYWORD_LIST = ','
KEYWORD_INVERSION = '!'
KEYWORD_NEGATIVE_MODIFIER = '-'
KEYWORD_POSITIVE_MODIFIER = '+'
KEYWORD_INDEX = '#'

MODIFIERS_RANGE = set(range(0, 366))

MINUTE_RANGE = set(range(0, 60))
HOUR_RANGE = set(range(0, 24))
DOM_RANGE = set(range(1, 32))
MONTH_RANGE = set(range(1, 13))
DOW_RANGE = set(range(1, 8))

MONTH_ALIASES = {
    'JAN': {1},
    'FEB': {2},
    'MAR': {3},
    'APR': {4},
    'MAY': {5},
    'JUN': {6},
    'JUI': {7},
    'AUG': {8},
    'SEP': {9},
    'OCT': {10},
    'NOV': {11},
    'DEC': {12},
}

DOW_ALIASES = {
    'MON': {1},
    'TUE': {2},
    'WED': {3},
    'THU': {4},
    'FRI': {5},
    'SAT': {6},
    'SUN': {7},
}
DOW_INDEX_RANGE = set(range(1, 6))


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

    if value[0].isalpha():
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
    elements = expression.split(KEYWORD_RANGE)
    if len(elements) != 2:
        raise CroneeSyntaxError(f"Syntax error for the range '{expression}'")
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


def parse_step(expression: str, valid_range: set[int], aliases: Aliases) -> tuple[int, str]:
    """
    Parses a step expression and returns an integer step value within the valid range.

    :param expression: A string representing the step expression to be parsed, in the form of '*/step' where 'step' is a string that can be parsed by the parse_value function.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `step` argument.
    :return: an integer representing the parsed step value
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid
    :raises: CroneeValueError, if the step value is not valid
    """
    original_expression = str(expression)
    elements = expression.split(KEYWORD_STEP)
    if len(elements) != 2:
        raise CroneeSyntaxError(f"Syntax error for the step expression '{original_expression}'")
    expression, step_str = elements
    step_set = parse_value(step_str, valid_range, aliases)
    if len(step_set) != 1:
        raise CroneeValueError(f"Invalid step value for the expression '{original_expression}'")
    step = next(iter(step_set))
    mini = min(valid_range)
    return step, expression


def parse_inversion(expression: str) -> tuple[bool, str]:
    """
    Parses a string expression and returns a tuple indicating if the inversion keyword is present and the rest of the expression after the inversion keyword.

    :param expression: A string representing the expression to be parsed.
    :return: A tuple of a boolean and a string, where the boolean indicates if the inversion keyword is present in the expression and the string is the rest of the expression after the inversion keyword.
    """
    if expression.startswith(KEYWORD_INVERSION):
        return True, expression[1:]
    return False, expression


def parse_index(expression: str,
                value_range: set[int],
                value_aliases: Aliases,
                index_range: set[int],
                index_aliases: Aliases,
                validator: IndexValidator) -> Validator:
    """
    Parses a string expression for an index, and returns a function that validates if the current index is in the parsed values.

    :param expression: A string representing the expression to be parsed.
    :param value_range: A set of integers representing the valid range of values.
    :param value_aliases: A dictionary of string keys and set of integers values, representing possible aliases for the values argument.
    :param index_range: A set of integers representing the valid range of indices.
    :param index_aliases: A dictionary of string keys and set of integers values, representing possible aliases for the index argument.
    :param validator:  A function that takes an index and values as input and returns a bool indicating whether the current index is in the parsed values or not.
    :return: A function that takes no input and returns a bool indicating whether the current index is in the parsed values or not.
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid.
    :raises: CroneeValueError, if the index or value  is not valid.
    """
    original_expression = str(expression)
    elements = expression.split(KEYWORD_INDEX)
    if len(elements) != 2:
        raise CroneeSyntaxError(f"Syntax error for the index expression '{original_expression}'")
    expression, index = elements
    index = parse_value(index, index_range, index_aliases)
    if len(index) != 1:
        raise CroneeValueError(f"Invalid index value for the expression '{original_expression}'")
    values = parse_value(expression, value_range, value_aliases)
    index = next(iter(index))
    return partial(validator, index=index, values=values)


def parse_modifier(expression, coef: int, keyword: str, aliases: Aliases) -> tuple[int, str]:
    """
    Parses a string expression for a modifier keyword and returns a tuple indicating the coefficient of the modifier multiplied by the modifier value and the rest of the expression after the modifier keyword.

    :param expression: A string representing the expression to be parsed.
    :param coef: An integer representing the coefficient of the modifier.
    :param keyword: A string representing the keyword of the modifier.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `modifier` argument.
    :return: A tuple of an integer and a string, where the integer indicates the modifier, and the string is the rest of the expression before the modifier keyword.
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid
    :raises: CroneeValueError, if the modifier value is not valid
    """
    original_expression = expression
    elements = expression.split(keyword)
    if len(elements) == 1:
        return 0, expression
    if len(elements) != 2:
        raise CroneeSyntaxError(f"Invalid modifier syntax '{original_expression}'")
    expression, modifier_str = elements
    modifier_set = parse_value(modifier_str, MODIFIERS_RANGE, aliases)
    if len(modifier_set) != 1:
        raise CroneeValueError(f"Invalid modifier value '{original_expression}'")
    modifier = next(iter(modifier_set))
    return coef * modifier, expression


def parse_modifiers(expression: str, aliases: Aliases) -> tuple[int, str]:
    """
    Parses a string expression for positive and negative modifiers and returns a tuple indicating the sum of the coefficients of the positive and negative modifier multiplied by their respective modifier values and the rest of the expression after the modifier keywords.

    :param expression: A string representing the expression to be parsed.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `positive` and `negative` modifier arguments.
    :return: A tuple of an integer and a string, where the integer indicates the modifier, and the string is the rest of the expression before the modifier keywords.
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid or if there is more than one modifier in the same field.
    :raises: CroneeValueError, if the positive or negative modifier values are not valid
    """
    if KEYWORD_NEGATIVE_MODIFIER in expression and KEYWORD_POSITIVE_MODIFIER in expression:
        raise CroneeSyntaxError(f"Cannot have more than one modifier in the same field. Invalid field '{expression}'")
    positive_modifier, expression = parse_modifier(expression, -1, KEYWORD_POSITIVE_MODIFIER, aliases)
    negative_modifier, expression = parse_modifier(expression, 1, KEYWORD_NEGATIVE_MODIFIER, aliases)
    return positive_modifier + negative_modifier, expression


def parse_generic_element(expression: str,
                          valid_range: set[int],
                          aliases: Aliases) -> tuple[Optional[Validator], set[int]]:
    """
    Parses a string expression for a value or a range of values within a given valid range, applies step and/or inversion to the parsed values, and returns the parsed values as a set of integers.

    :param expression: A string representing the expression to be parsed.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `value` argument.
    :return: a set of integers representing the parsed value.
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid or if there is a step and a range in the same field or if there is an inversion keyword in the range
    :raises: CroneeValueError, if the  step value is not valid
    :raises: CroneeOutOfBoundError, if the `value` or `stop` or `start` argument is out of the valid range
    :raises: CroneeRangeOrderError, if the `start` value is greater than the `stop` value
    :raises: CroneeAliasError, if the `value` argument is not in the provided aliases
    """
    step = 1
    if KEYWORD_STEP in expression:
        step, expression = parse_step(expression, valid_range, aliases)

    if KEYWORD_RANGE in expression:
        values = parse_range(expression, valid_range, aliases)
    else:
        values = parse_value(expression, valid_range, aliases)

    mini = min(values)
    values = set(filter(lambda v: v % step == mini % step, values))
    return None, values


def parse_dow_element(expression: str,
                      valid_range: set[int],
                      aliases: Aliases) -> tuple[Optional[Validator], set[int]]:
    """
    Parses a string expression for a value or a range of values within a given valid range or index, applies step and/or inversion to the parsed values, and returns the parsed values as a set of integers.

    :param expression: A string representing the expression to be parsed.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `value` argument.
    :return: a set of integers representing the parsed value.
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid or if there is a step and a range in the same field or if there is an inversion keyword in the range
    :raises: CroneeValueError, if the  step value is not valid
    :raises: CroneeOutOfBoundError, if the `value` or `stop` or `start` argument is out of the valid range
    :raises: CroneeRangeOrderError, if the `start` value is greater than the `stop` value
    :raises: CroneeAliasError, if the `value` argument is not in the provided aliases
    """
    validator = None
    step = 1
    if KEYWORD_STEP in expression:
        step, expression = parse_step(expression, valid_range, aliases)

    if KEYWORD_RANGE in expression:
        values = parse_range(expression, valid_range, aliases)
    elif KEYWORD_INDEX in expression:
        return parse_index(expression, valid_range, aliases, DOW_INDEX_RANGE, {}, dow_index_validator), set()
    else:
        values = parse_value(expression, valid_range, aliases)

    mini = min(values)
    values = set(filter(lambda v: v % step == mini % step, values))
    return validator, values


def parse_field(expression: str,
                valid_range: set[int],
                value_aliases: Aliases,
                step_aliases: Aliases,
                element_parser: ElementParser,
                allow_empty: bool = False) -> tuple[int, list[Validator], set[int]]:
    """
        Parses a string expression for a field and returns a tuple of the parsed values and a set of integers within a given valid range. The parsed values can be modified by positive and negative modifiers, inverted, and be a list of values and ranges.

        :param expression: A string representing the expression to be parsed.
        :param valid_range: A set of integers representing the valid range of values.
        :param value_aliases: A dictionary of string keys and set of integers values, representing possible aliases for the `value` argument.
        :param step_aliases: A dictionary of string keys and set of integers values, representing possible aliases for the `step` argument.
        :param element_parser: A callable that takes a string `expression`, a `valid_range` and `value_aliases` as arguments and returns a set of integers
        :return: a tuple of the parsed values ( an int indicating the sum of the coefficients of the positive and negative modifier multiplied by their respective modifier values) and a set of integers representing the parsed value.
        :raises: CroneeEmptyValuesError, if the parsed values set is empty.
        :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid or if there is more than one modifier in the same field
        :raises: CroneeValueError, if the step or value or start or stop or modifier values are not valid.
        """
    modifier, expression = parse_modifiers(expression, step_aliases)
    inversion, expression = parse_inversion(expression)

    validators = []
    values = set()
    elements = expression.split(KEYWORD_LIST)
    for element in elements:
        element_validator, element_values = element_parser(element, valid_range, value_aliases)
        values = values.union(element_values)
        if element_validator is not None:
            validators.append(element_validator)

    if inversion:
        values = valid_range.difference(values)

    if len(values) == 0 and not allow_empty:
        raise CroneeEmptyValuesError(f"No valid values for the expression '{expression}'")

    return modifier, validators, values


def parse_expression(expression: str) -> Cronee:
    """
    Parse a cron-like expression and returns an instance of Cronee.

    :param expression: A string representing the cron-like expression to be parsed.
    :return: An instance of Cronee representing the parsed expression.
    :raises: CroneeSyntaxError, if the number of fields in the expression is different from 5.
    """
    fields = shlex.split(expression)
    if len(fields) != 5:
        raise CroneeSyntaxError(f'Invalid number of field. A cronee must have 5 fields.')

    min_modifier, min_validators, min_values = parse_field(fields[0], MINUTE_RANGE, {}, {}, parse_generic_element)
    hou_modifier, hou_validators, hou_values = parse_field(fields[1], HOUR_RANGE, {}, {}, parse_generic_element)
    dom_modifier, dom_validators, dom_values = parse_field(fields[2], DOM_RANGE, {}, {}, parse_generic_element)
    mon_modifier, mon_validators, mon_values = parse_field(fields[3], MONTH_RANGE, MONTH_ALIASES, {},
                                                           parse_generic_element)
    dow_modifier, dow_validators, dow_values = parse_field(fields[4], DOW_RANGE, DOW_ALIASES, {}, parse_dow_element,
                                                           True)

    modifier = timedelta(days=dom_modifier + dow_modifier, hours=hou_modifier, minutes=min_modifier)
    validators = [min_validators, hou_validators, dom_validators, mon_validators, dow_validators]

    return SimpleCronee(
        minutes=min_values,
        hours=hou_values,
        doms=dom_values,
        months=mon_values,
        dows=dow_values,
        offset=modifier,
        other_validators=validators
    )
