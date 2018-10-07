import argparse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QPixmap, QImage
from reversi import driver, game, gamefield, gui


def start_app(game_driver):
    app = QApplication(sys.argv)

    main_window = gui.ReversiWindow(game_driver)
    main_window.show()

    sys.exit(app.exec_())


def parse_args():
    pass


def main():
    args = parse_args()
    game_driver = driver.GameDriver()
    start_app(game_driver)


if __name__ == "__main__":
    main()
