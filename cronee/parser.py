from .exceptions import CroneeOutOfBoundError, CroneeAliasError, CroneeValueError, CroneeRangeOrderError, \
    CroneeSyntaxError

Aliases = dict[str, set[int]]

TOKEN_JOKER = '*'
KEYWORD_RANGE = '..'
KEYWORD_STEP = '/'
KEYWORD_LIST = ','
KEYWORD_INVERSION = '!'
KEYWORD_NEGATIVE_MODIFIER = '-'
KEYWORD_POSITIVE_MODIFIER = '+'

MODIFIERS_RANGE = set(range(0, 366))


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


def parse_step(expression: str, valid_range: set[int], aliases: Aliases) -> int:
    """
    Parses a step expression and returns an integer step value within the valid range.

    :param expression: A string representing the step expression to be parsed, in the form of '*/step' where 'step' is a string that can be parsed by the parse_value function.
    :param valid_range: A set of integers representing the valid range of values.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `step` argument.
    :return: an integer representing the parsed step value
    :raises: CroneeSyntaxError, if the syntax of the `expression` argument is invalid
    :raises: CroneeValueError, if the step value is not valid
    """
    elements = expression.split(KEYWORD_STEP)
    if len(elements) != 2:
        raise CroneeSyntaxError(f"Syntax error for the step expression '{expression}'")
    _, step_str = elements
    step_set = parse_value(step_str, valid_range, aliases)
    if len(step_set) != 1:
        raise CroneeValueError(f"Invalid step value for the expression '{expression}'")
    step = next(iter(step_set))
    return step


def parse_inversion(expression: str) -> tuple[bool, str]:
    """
    Parses a string expression and returns a tuple indicating if the inversion keyword is present and the rest of the expression after the inversion keyword.

    :param expression: A string representing the expression to be parsed.
    :return: A tuple of a boolean and a string, where the boolean indicates if the inversion keyword is present in the expression and the string is the rest of the expression after the inversion keyword.
    """
    if expression.startswith(KEYWORD_INVERSION):
        return True, expression[1:]
    return False, expression


def parse_modifier(expression, coef: int, keyword: str, aliases: Aliases) -> tuple[int, str]:
    """
    Parses a string expression for a modifier keyword and returns a tuple indicating the coefficient of the modifier multiplied by the modifier value and the rest of the expression after the modifier keyword.

    :param expression: A string representing the expression to be parsed.
    :param coef: An integer representing the coefficient of the modifier.
    :param keyword: A string representing the keyword of the modifier.
    :param aliases: (optional) A dictionary of string keys and set of integers values, representing possible aliases for the `modifier` argument.
    :return: A tuple of an integer and a string, where the integer indicates the coefficient of the modifier multiplied by the modifier value, and the string is the rest of the expression after the modifier keyword.
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


# def parse_field(expression: str, valid_range: set[int], aliases: Aliases) -> tuple[int, set[int]]:
#     original_expression = str(expression)
#     inversion, expression = parse_inversion(expression)
#     elements = expression.split(KEYWORD_LIST)
