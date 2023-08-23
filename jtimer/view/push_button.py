from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton
from jtimer.view import BACKGROUND_COLOR


class PushButton(QPushButton):
    def __init__(self, icon: str):
        super().__init__()
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; ")
        self.setIcon(QIcon(icon))
        self.setFixedSize(30, 30)
