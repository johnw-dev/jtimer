from PyQt6.QtWidgets import (
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QWidget,
)
from PyQt6.QtCore import Qt, QSize

from jtimer.controller import ControllerInterface as Controller
from jtimer.view import ADD_ICON, CHART_ICON
from jtimer.view.push_button import PushButton
from jtimer.view.timer_widget import TimerWidget
from jtimer.model.timer import Timer
import logging
from functools import reduce

LOG = logging.getLogger("TimersView")


class TimersView(QWidget):
    def __init__(self, controller: Controller):
        super().__init__()
        self.lineEdit = None
        self.timer_widgets = {}
        self.controller = controller
        main_layout = QVBoxLayout()

        self.timer_list = QVBoxLayout()
        self.timer_list.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.timer_list.setSpacing(0)
        main_layout.addLayout(self.build_menu())
        main_layout.addLayout(self.timer_list)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(main_layout)
        self.refresh()

    def build_menu(self) -> QBoxLayout:
        menu = QHBoxLayout()
        menu.setAlignment(Qt.AlignmentFlag.AlignLeft)
        menu.setSpacing(2)
        menu.setContentsMargins(6, 3, 6, 3)

        add_button = PushButton(ADD_ICON)
        add_button.clicked.connect(self.add_button_click)

        self.lineEdit = QLineEdit("zzz")

        view_stats_button = PushButton(CHART_ICON)
        view_stats_button.clicked.connect(self.controller.show_stats)

        menu.addWidget(add_button)
        menu.addWidget(self.lineEdit)
        menu.addWidget(view_stats_button)
        return menu

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.add_button_click()
        super().keyPressEvent(event)

    def add_button_click(self):
        name = f"{self.lineEdit.text()}"
        self.controller.new_timer(name)

    def add_timer(self, new_timer: Timer):
        widget = TimerWidget(new_timer, self.controller)
        self.timer_list.addWidget(widget)
        self.timer_widgets[new_timer.name] = widget
        self.refresh()

    def delete_timer(self, timer: str):
        widget = self.timer_widgets[timer]
        self.timer_list.removeWidget(widget)
        self.timer_widgets.pop(timer, None)
        self.refresh()

    def refresh(self):
        """resize window to fit content width"""
        if len(self.timer_widgets.keys()):
            max = reduce(get_max, self.timer_widgets.keys())
            estimated_width = self.timer_widgets.get(max).get_width()
            width = self.size().width()
            if width < estimated_width or width - 100 > estimated_width:
                width = estimated_width
            height = len(self.timer_widgets.keys()) * 35
            new_size = QSize(width, height)
            self.window().resize(new_size)
            LOG.debug(
                f"resized:  {width.real}, {height.real}, {len(self.timer_widgets.keys())}"
            )


def get_max(a: str, b: str) -> str:
    if len(a) > len(b):
        return a
    else:
        return b
