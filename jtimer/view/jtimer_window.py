from PyQt6.QtCore import Qt, QCoreApplication as App
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon

from jtimer.view import STOPWATCH_ICON, BACKGROUND_COLOR
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
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR}; ")
        self.show()

    def closeEvent(self, event):
        """Override to force exit when main window closed"""
        event.accept()
        App.exit(0)

    def keyPressEvent(self, event):
        """Close application from escape key."""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
