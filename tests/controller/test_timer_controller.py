from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, MagicMock

from jtimer.model.timer import Timer
from jtimer.model.time_event import TimeEvent, TimeEventType


class ControllerTest(TestCase):
    @patch("jtimer.view.timers_view.TimersView")
    @patch("jtimer.view.jtimer_window.JTimerWindow")
    def test_constructor_should_not_set_timers_when_dao_lookup_returns_empty(
        self, window_mock, view_mock
    ):
        import jtimer.controller.timer_controller as module

        dao_mock = MagicMock()
        dao_mock.get_all_timer_objects.return_value = []
        testee = module.TimerController(dao_mock)
        dao_mock.get_all_timer_objects.assert_called()
        self.assertEqual({}, testee.timers)

    @patch("jtimer.view.timers_view.TimersView")
    @patch("jtimer.view.jtimer_window.JTimerWindow")
    def test_constructor_should_add_timer_when_timer_returned_from_dao(
        self, window_mock, view_mock
    ):
        import jtimer.controller.timer_controller as module

        dao_mock = MagicMock()
        dao_mock.get_all_timer_objects.return_value = [Timer(id, "foobar", [])]
        dao_mock.get_last_event.return_value = None
        testee = module.TimerController(dao_mock)

        dao_mock.get_all_timer_objects.assert_called()
        stored_timer = testee.timers.get("foobar")
        self.assertEqual("foobar", stored_timer.name)
        self.assertEqual([], stored_timer.events)

    @patch("jtimer.view.timers_view.TimersView")
    @patch("jtimer.view.jtimer_window.JTimerWindow")
    def test_constructor_should_stop_timers_if_last_event_was_active_and_not_today(
        self, window_mock, view_mock
    ):
        import jtimer.controller.timer_controller as module

        event = TimeEvent(
            TimeEventType.START,
            datetime.now() - timedelta(days=2),
        )
        dao_mock = MagicMock()
        dao_mock.get_all_timer_objects.return_value = [
            Timer(
                id,
                "foobar",
                [event],
            )
        ]
        dao_mock.get_last_event.return_value = event
        testee = module.TimerController(dao_mock)

        dao_mock.get_all_timer_objects.assert_called()
        dao_mock.create_event.assert_called()
        stored_timer = testee.timers.get("foobar")
        self.assertEqual("foobar", stored_timer.name)
        self.assertEqual(2, len(stored_timer.events))

    @patch("jtimer.view.timers_view.TimersView")
    @patch("jtimer.view.jtimer_window.JTimerWindow")
    def test_stop_forgotten_timers_should_add_event_when_last_event_yesterday_and_not_stopped(
        self, window_mock, view_mock
    ):
        import jtimer.controller.timer_controller as module

        dao_mock = MagicMock()
        dao_mock.get_all_timer_objects.return_value = []
        testee = module.TimerController(dao_mock)

        input_timer = Timer(0, "foobar", [])
        event = TimeEvent(
            TimeEventType.START,
            datetime.now() - timedelta(days=1),
        )
        result = testee.__stop_forgotten_timers__(input_timer, [event])
        self.assertEqual(1, result)
        dao_mock.create_event.assert_called()
