from datetime import timedelta, datetime, date
import unittest
from mptimer.model.time_event import TimeEvent, TimeEventType
from mptimer.controller.calc_utils import eod, happened_on_day, sod


class TestTimer(unittest.TestCase):
    def test_happened_on_day_should_return_true_when_created_matches_date(self):
        event = TimeEvent(TimeEventType.START, datetime.now())
        self.assertEqual(True, happened_on_day(event, date.today()))

    def test_happened_on_day_should_return_false_when_created_does_not_match_date(self):
        event = TimeEvent(TimeEventType.START, datetime.now() - timedelta(days=1))
        self.assertEqual(False, happened_on_day(event, date.today()))

    def test_eod(self):
        input = datetime.fromisoformat("2011-11-04 00:05:23.283")
        expected = datetime.fromisoformat("2011-11-04 23:59:59.999999")

        self.assertEqual(expected, eod(input))

    def test_sod(self):
        input = datetime.fromisoformat("2011-11-04 00:05:23.283")
        expected = datetime.fromisoformat("2011-11-04 00:00:00.000000")

        self.assertEqual(expected, sod(input))
