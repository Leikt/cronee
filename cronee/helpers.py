from datetime import datetime, timedelta
from calendar import monthrange



def dom_delta(field_values: set[int], start: datetime) -> int:
    number_of_days = monthrange(start.year, start.month)[1]
    next_valid_value = min(filter(lambda v: start.day <= v <= number_of_days, field_values), default=None)
    if next_valid_value is not None:
        return next_valid_value - start.day

    delta_to_end_of_month = number_of_days - start.day
    start += timedelta(days=delta_to_end_of_month)
    return dom_delta(field_values, start)
