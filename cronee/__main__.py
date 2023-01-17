import argparse
import datetime

from .parser import parse_expression


def datetime_args(value: str) -> datetime:
    if value == 'now':
        return datetime.datetime.now()
    return datetime.datetime.strptime(value, "%H:%M %d-%m-%Y")


parser = argparse.ArgumentParser(prog="Cronee")
parser.description = "Cronee (CRON Extended Expression) is a tool that validates datetime against a Cronee Expression."
parser.add_argument('expression', type=str, help="Cronee expression to parse")
group_next_occurrences = parser.add_argument_group()
group_next_occurrences.title = "Compute next occurrences"
group_next_occurrences.set_defaults(next_occurrences=10)
group_next_occurrences.add_argument('-n', '--next-occurrences', type=int, default=10,
                                    help="Number of next occurrences to display.")
group_next_occurrences.add_argument('-s', '--start-date', type=datetime_args, default=None, metavar="HH:MM dd-mm-YYYY",
                                    help="Start date for the next occurrences computation.")

group_validation = parser.add_argument_group()
group_validation.title = "Validate a certain date"
group_validation.add_argument('-d', '--date', type=datetime_args, default=None, metavar="HH:MM dd-mm-YYYY",
                              help="Date to validate.")

parser.add_argument('-o', '--output', choices=['python', 'yaml', 'shell', 'verbose'], default='shell',
                    help="Transform the output to match the given choice.")

args = parser.parse_args()

try:
    cronee_validator = parse_expression(args.expression)
except Exception as e:
    print(f"{type(e).__name__}: {e}")
    exit(1)

if args.date is not None:
    result = cronee_validator.validate(args.date)
    if args.output == 'python':
        print(result)
    elif args.output == 'yaml':
        print(str(result).lower())
    elif args.output == 'shell':
        print(0 if result else 1)
    elif args.output == 'verbose':
        if result:
            print(f'{args.date.strftime("%H:%M %d-%m-%Y")} validates the expression "{args.expression}"')
        else:
            print(f'{args.date.strftime("%H:%M %d-%m-%Y")} doesn\'t validates the expression "{args.expression}"')

if args.start_date is not None:
    result = cronee_validator.next_occurrences(args.start_date, args.next_occurrences)
    if args.output == 'python':
        print(result)
    elif args.output == 'yaml':
        for date in result:
            print(f'- "date.strftime("%H:%M %d-%m-%Y")"')
    elif args.output == 'shell':
        res = '(' + \
              ' '.join([f'"{date.strftime("%H:%M %d-%m-%Y")}"' for date in result]) \
              + ')'
        print(res)
    elif args.output == 'verbose':
        print(
            f'Next {args.next_occurrences} occurrences of {args.expression} from {args.start_date.strftime("%H:%M %d-%m-%Y"):}')
        for date in result:
            print(f'- {date.strftime("%H:%M %d-%m-%Y")}')
