import os
import argparse
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from jtimer.controller.timer_controller import TimerController
from jtimer.dao import DAO
import logging


def create_path(file: str):
    path = Path(file)
    if not path.parent.exists():
        path.parent.mkdir()


def start():
    parser = argparse.ArgumentParser(
        prog="jtimer",
        description="John's Timer - desktop app for tracking time",
        epilog="Text at the bottom of help",
    )
    parser.add_argument(
        "-d",
        "--db",
        dest="db",
        default=os.path.expanduser("~/.jtimer/jtimer.db"),
        help="location of database (~/jtimer/jtimer.db)",
    )
    parser.add_argument(
        "-l",
        "--log_level",
        dest="log_level",
        default="WARNING",
        help="Level of console logging (WARNING)",
    )
    args = parser.parse_args()
    logging.basicConfig(encoding="utf-8", level=args.log_level)

    App = QApplication([])

    create_path(args.db)
    controller = TimerController(DAO(args.db))
    App.exit(App.exec())


if __name__ == "__main__":
    start()
