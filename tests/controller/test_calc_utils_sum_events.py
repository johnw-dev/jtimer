from datetime import timedelta, datetime
import unittest
from jtimer.model.time_event import TimeEvent, TimeEventType
from jtimer.controller.calc_utils import sum_events


class TestTimer(unittest.TestCase):
    def test_sum_events_should_return_0_when_empty(self):
        input = []
        self.assertEqual(timedelta(), sum_events(input), "sum should be 0")

    def test_sum_events_should_return_0_when_None(self):
        input = None
        self.assertEqual(timedelta(), sum_events(input), "sum should be 0")

    def test_sum_events_should_return_0_when_events_do_not_have_delta(self):
        now = datetime.now()
        start = TimeEvent(type=TimeEventType.START, created=now)
        stop = TimeEvent(type=TimeEventType.STOP, created=now)
        input = [start, stop]
        self.assertEqual(timedelta(), sum_events(input), "sum should be 0")

    def test_sum_events_should_return_result_when_single_delta(self):
        now = datetime.now()
        delta = timedelta(seconds=5)
        start = TimeEvent(type=TimeEventType.START, created=now)
        stop = TimeEvent(type=TimeEventType.STOP, created=now + delta)
        input = [start, stop]
        self.assertEqual(delta, sum_events(input), "sum should be 5s")

    def test_sum_events_should_return_result_when_multiple_deltas(self):
        now = datetime.now()
        delta = timedelta(seconds=5)
        start1 = TimeEvent(type=TimeEventType.START, created=now)
        stop1 = TimeEvent(type=TimeEventType.STOP, created=now + delta)

        start2 = TimeEvent(type=TimeEventType.START, created=now)
        stop2 = TimeEvent(type=TimeEventType.STOP, created=now + delta)

        input = [start1, stop1, start2, stop2]
        self.assertEqual(delta + delta, sum_events(input), "sum should be 10s")

    def test_sum_events_should_return_result_when_last_event_is_start_including_difference_in_time(
        self,
    ):
        now = datetime.now()
        start1 = TimeEvent(
            type=TimeEventType.START, created=now - timedelta(seconds=60)
        )
        stop1 = TimeEvent(type=TimeEventType.STOP, created=now - timedelta(seconds=50))
        start2 = TimeEvent(type=TimeEventType.START, created=now - timedelta(seconds=5))

        input = [start1, stop1, start2]
        self.assertEqual(
            timedelta(seconds=15).seconds,
            sum_events(input).seconds,
            "sum should be 15s",
        )

    def test_sum_events_should_return_result_when_first_result_is_stop(self):
        now = datetime.now()
        stop1 = TimeEvent(type=TimeEventType.STOP, created=now)

        input = [stop1]
        self.assertEqual(timedelta(), sum_events(input), "sum should be 0s")
