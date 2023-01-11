import unittest
from cronee import CroneeSyntaxError, CroneeValueError
from cronee.parser import parse_step


class TestParseStep(unittest.TestCase):
    def test_valid_input(self):
        step = parse_step('*/5', set(range(0, 100)), {})
        self.assertEqual(5, step)

    def test_valid_alias(self):
        step = parse_step('*/TRIM', set(range(0, 100)), {'TRIM': {3}})
        self.assertEqual(3, step)

    def test_syntax_error(self):
        with self.assertRaises(CroneeSyntaxError):
            parse_step('*//3', set(), {})

    def test_value_error(self):
        with self.assertRaises(CroneeValueError):
            parse_step('*/ERR', set(range(0, 10)), {'ERR': {1, 2, 3}})
