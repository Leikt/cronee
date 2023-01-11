class CroneeValueError(Exception):
    """Exception raised when a syntax error is detected."""


class CroneeAliasError(Exception):
    """Exception raised when an alias is unknown."""


class CroneeOutOfBoundError(Exception):
    """Exception raised when a value is out of the valid values accepted for the field."""


class CroneeSyntaxError(Exception):
    """Exception raised when the syntax is invalid."""
