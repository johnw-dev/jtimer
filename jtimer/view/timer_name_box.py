from PyQt6.QtWidgets import QLineEdit

from jtimer.controller import ControllerInterface as Controller
from jtimer.view import BOLD_LABEL_STYLE, NORMAL_LABEL_STYLE


class TimerNameBox(QLineEdit):
    def __init__(self, name, controller: Controller):
        super().__init__(name)
        self.timer_name = name
        self.controller = controller
        self.normal_style()
        self.setFixedHeight(28)

    def focusOutEvent(self, e):
        self.controller.update_timer(self.timer_name, self.text())
        super().focusOutEvent(e)

    def bold_style(self):
        self.setStyleSheet(BOLD_LABEL_STYLE)

    def normal_style(self):
        self.setStyleSheet(NORMAL_LABEL_STYLE)

    def estimate_width(self):
        return self.fontMetrics().boundingRect(self.text()).width() + 20
