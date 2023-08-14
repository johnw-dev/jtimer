from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from jtimer.view import STOPWATCH_ICON
from jtimer.view.timers_view import TimersView

from jtimer.controller import ControllerInterface as Controller


class JTimerWindow(QMainWindow):
    def __init__(
        self,
        controller: Controller,
    ) -> None:
        super().__init__()
        self.controller = controller
        self.view = TimersView(controller)
        self.setWindowTitle("JTimer")
        self.setWindowIcon(QIcon(STOPWATCH_ICON))
        self.setCentralWidget(self.view)
        self.show()
