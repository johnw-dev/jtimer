import sys
from PyQt6.QtWidgets import QApplication
from mptimer.controller.timer_controller import TimerController
from mptimer.dao import DAO

if __name__ == "__main__":
    App = QApplication(sys.argv)
    controller = TimerController(DAO("timer.db"))
    App.exit(App.exec())
