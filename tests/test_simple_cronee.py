import unittest
from cronee import parse_expression
from cronee.cronee import SimpleCronee
from helpers import easy_datetime


class TestSimpleCronee(unittest.TestCase):
    def test_dummy_expression(self):
        c = parse_expression('* * * * *')
        self.assertIsInstance(c, SimpleCronee)
        self.assertTrue(c.validate(easy_datetime()))

    def test_simple_numerical_expression(self):
        c = parse_expression('1 2 3 4 *')
        self.assertTrue(c.validate(easy_datetime(minute=1, hour=2, day=3, month=4)))
        self.assertFalse(c.validate(easy_datetime(minute=2)))

    def test_simple_range_expression(self):
        c = parse_expression('1..30 5..8 1..6 2..3 *')
        self.assertTrue(c.validate(easy_datetime(minute=2, hour=8, day=5, month=2)))
        self.assertFalse(c.validate(easy_datetime(minute=55)))

    def test_simple_step_expression(self):
        c = parse_expression('*/10 */5 */3 */5 *')
        self.assertTrue(c.validate(easy_datetime(minute=10, hour=15, day=28, month=11)))
        self.assertFalse(c.validate(easy_datetime(minute=55)))

    def test_simple_index_dow(self):
        c = parse_expression('* * * * FRI#3')
        self.assertTrue(c.validate(easy_datetime(year=2023, month=1, day=20)))
        self.assertFalse(c.validate(easy_datetime(year=2023, month=1, day=2)))

    def test_simple_modifier(self):
        c = parse_expression('* * 15-1 * *')
        self.assertTrue(c.validate(easy_datetime(day=14)))

    def test_complex_expression_1(self):
        c = parse_expression('!0..30/5,45 5,15..23/3 15,1-1 !JAN,MAR,JUN,OCT *')
        self.assertTrue(c.validate(easy_datetime(year=2023, month=7, day=31, hour=18, minute=44)))
        self.assertTrue(c.validate(easy_datetime(year=2023, month=7, day=14, hour=18, minute=44)))
        self.assertTrue(c.validate(easy_datetime(year=2023, month=9, day=14, hour=18, minute=44)))

        self.assertFalse(c.validate(easy_datetime(year=2023, month=10, day=14, hour=18, minute=44)))

    def test_complex_expression_2(self):
        c = parse_expression('0..5 8 * * FRI#3,SUN#4')
        self.assertTrue(c.validate(easy_datetime(year=2023, month=1, day=20, hour=8, minute=3)))
        self.assertTrue(c.validate(easy_datetime(year=2023, month=1, day=22, hour=8, minute=5)))
        self.assertFalse(c.validate(easy_datetime(year=2023, month=1, day=1, hour=8, minute=3)))

    def test_complex_expression_3(self):
        c = parse_expression('* * 1-1 FEB,MAR *')
        self.assertTrue(c.validate(easy_datetime(year=2023, month=1, day=31)))

        # Special case: february
        self.assertTrue(c.validate(easy_datetime(year=2023, month=2, day=28)))

    def test_last_day_of_the_month(self):
        c = parse_expression('* * 1-1 * *')
        self.assertTrue(c.validate(easy_datetime(year=2023, month=1, day=31)))
        self.assertTrue(c.validate(easy_datetime(year=2023, month=7, day=31)))
        self.assertTrue(c.validate(easy_datetime(year=2023, month=6, day=30)))

        # Special case: february
        self.assertTrue(c.validate(easy_datetime(year=2023, month=2, day=28)))
