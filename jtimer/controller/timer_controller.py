from datetime import date, timedelta
from jtimer.model.time_event import TimeEvent, TimeEventType
from jtimer.controller.calc_utils import happened_on_day, sum_events, eod
from jtimer.view.stats_view import StatsView
from jtimer.dao import DAO
from jtimer.model.timer import Timer
from jtimer.controller import ControllerInterface
from jtimer.view.timers_view import TimersView

from jtimer.view.jtimer_window import JTimerWindow
import logging

LOG = logging.getLogger("TimerController")


class TimerController(ControllerInterface):
    def __init__(self, dao: DAO):
        super().__init__()
        self.stats_view = None
        self.dao = dao
        timers = self.dao.get_all_timer_objects()
        self.timers = {}
        self.window: JTimerWindow = JTimerWindow(controller=self)
        self.view: TimersView = self.window.view
        self.window.show()
        for t in timers:
            timer: Timer = t
            timer.delta = sum_events(timer.events)
            last_event = self.dao.get_last_event(timer.id)
            if last_event:
                timer.events.append(last_event)
            self.__stop_forgotten_timers__(timer, [last_event])
            self.__add_timer__(timer)

    def __add_timer__(self, timer: Timer):
        self.timers[timer.name] = timer
        self.view.add_timer(timer)

    def __stop_forgotten_timers__(self, timer: Timer, events: list) -> int:
        modified = 0
        if events:
            for idx, e in enumerate(events):
                event: TimeEvent = e
                if event and event.type == TimeEventType.START:
                    if not happened_on_day(event, date.today()):
                        LOG.debug("stopping forgotten timer", event.created)
                        new_event = TimeEvent(
                            TimeEventType.STOP, eod(event.created.date())
                        )
                        self.dao.create_event(timer, new_event)
                        events.append(new_event)
                        modified = 1
        return modified

    def new_timer(self, name: str):
        if len(name) > 0:
            if not self.timers.get(name):
                timer = self.dao.create_timer(name)
                self.__add_timer__(timer)
            else:
                LOG.debug("not adding timer: exists already")
        else:
            LOG.debug("not adding timer: no name")

    def update_timer(self, name: str, new_name: str):
        if self.timers.get(name) and new_name:
            timer: Timer = self.timers[name]
            timer.name = new_name
            self.dao.update_timer(timer)

    def delete_timer(self, name: str):
        timer = self.timers.get(name)
        if timer:
            self.timers.pop(name)
            self.dao.delete_timer(timer)
            self.view.delete_timer(name)

    def add_event(self, name: str, event: TimeEvent):
        if self.timers.get(name):
            self.dao.create_event(self.timers[name], event)

    def show_stats(self):
        today = date.today()
        timer_stats = {}
        for key in self.timers.keys():
            timer: Timer = self.timers[key]
            daily_totals = []
            for i in reversed(range(0, 7)):
                day = today - timedelta(days=i)
                events = self.dao.get_all_events_for_day(timer.id, day)
                if self.__stop_forgotten_timers__(timer, events):
                    events = self.dao.get_all_events_for_day(timer.id, day)
                daily_totals.append((str(sum_events(events))).split(".")[0])
            timer_stats[key] = daily_totals
        LOG.debug("opening stats view")
        self.stats_view = StatsView(timer_stats)
        self.stats_view.show()
