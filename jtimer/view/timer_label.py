from PyQt6.QtWidgets import QLabel

from jtimer.view import BOLD_LABEL_STYLE, NORMAL_LABEL_STYLE


class TimerLabel(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFixedHeight(28)
        self.normal_style()

    def bold_style(self):
        self.setStyleSheet(BOLD_LABEL_STYLE)

    def normal_style(self):
        self.setStyleSheet(NORMAL_LABEL_STYLE)

    def estimate_width(self):
        return self.fontMetrics().boundingRect(self.text()).width() + 10
