class CroneeValueError(Exception):
    """Exception raised when a syntax error is detected."""


class CroneeAliasError(Exception):
    """Exception raised when an alias is unknown."""


class CroneeOutOfBoundError(Exception):
    """Exception raised when a value is out of the valid values accepted for the field."""


class CroneeSyntaxError(Exception):
    """Exception raised when the syntax is invalid."""


class CroneeRangeOrderError(Exception):
    """Exception raised when the range has invalid start and stop values."""


class CroneeEmptyValuesError(Exception):
    """Exception raised when an expression leads to an empty set of valid values."""
