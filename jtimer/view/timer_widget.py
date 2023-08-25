from tkinter import EventType
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, Qt
from datetime import timedelta, datetime
from jtimer.model.time_event import TimeEvent, TimeEventType
from jtimer.model.timer import Timer
from jtimer.view import (
    DELETE_ICON,
    PLAY_ICON,
    PAUSE_ICON,
    BORDER_COLOR,
)
from jtimer.controller import ControllerInterface as Controller
from jtimer.view.push_button import PushButton
from jtimer.view.timer_label import TimerLabel
from jtimer.view.timer_name_box import TimerNameBox

DEFAULT_RESOLUTION_SECONDS = 1
DEFAULT_RESOLUTION_MS = DEFAULT_RESOLUTION_SECONDS * 1000
BORDER_STYLE = f"border: 1px solid {BORDER_COLOR};"


class TimerWidget(QWidget):
    def __init__(self, timer: Timer, controller: Controller):
        super().__init__()
        self.instance = timer
        self.controller = controller
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(6, 3, 6, 3)
        self.name_label = TimerNameBox(timer.name, self.controller)

        self.value_label = TimerLabel(str(timer.get_delta_str()))
        self.button = PushButton(PLAY_ICON)
        self.resolution_ms = DEFAULT_RESOLUTION_MS
        self.resolution_delta = timedelta(seconds=DEFAULT_RESOLUTION_SECONDS)

        self.button.clicked.connect(self.on_button_clicked)

        self.delete_button = PushButton(DELETE_ICON)
        self.delete_button.clicked.connect(self.delete)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.value_label)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.sleeper = QTimer(self)
        self.sleeper.timeout.connect(self.update_timer)
        if self.is_active():
            self.sleeper.start(self.resolution_ms)
            self.button.setIcon(QIcon(PAUSE_ICON))
            self.value_label.styleSheet()
            self.value_label.bold_style()
            self.name_label.bold_style()
        self.setLayout(self.layout)

    def on_button_clicked(self):
        event_time = datetime.now()
        if self.is_active():
            self.instance.state = 0
            self.sleeper.stop()
            self.button.setIcon(QIcon(PLAY_ICON))
            self.add_event(TimeEventType.STOP, event_time)
            self.value_label.normal_style()
            self.name_label.normal_style()

        else:
            self.instance.state = 1
            self.sleeper.start(self.resolution_ms)
            self.button.setIcon(QIcon(PAUSE_ICON))
            self.add_event(TimeEventType.START, event_time)
            self.value_label.bold_style()
            self.name_label.bold_style()

    def update_timer(self):
        self.instance.delta += self.resolution_delta
        self.value_label.setText(str(self.instance.get_delta_str()))

    def is_active(self):
        return self.instance.state

    def add_event(self, event_type: EventType, event_time: datetime):
        event = TimeEvent(event_type, event_time)
        self.instance.events.append(event)
        self.controller.add_event(self.instance.name, event)

    def delete(self):
        check = QMessageBox.question(
            self,
            f"Delete {self.instance.name}?",
            f"are you sure you want to delete this timer? {self.instance.name}",
        )
        if check == check.Yes:
            if self.is_active():
                self.on_button_clicked()
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)
            self.setParent(None)
            self.controller.delete_timer(self.instance.name)

    def get_width(self):
        name_width = self.name_label.estimate_width()
        button_width = self.button.width()
        value_width = self.value_label.estimate_width()
        delete_width = self.delete_button.width()
        margins = (
            self.layout.contentsMargins().left() + self.layout.contentsMargins().right()
        )
        spacing = self.layout.spacing() * 10
        return (
            name_width + button_width + delete_width + value_width + margins + spacing
        )
