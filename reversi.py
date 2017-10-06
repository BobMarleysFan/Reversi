import argparse
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFrame, QGridLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtGui import QIcon, QPixmap, QImage
from reversi import driver, game, gamefield

PICTURE_FROM_CELLSTATE = {
    gamefield.DiskType.BLACK: "pictures/black.png",
    gamefield.DiskType.WHITE: "pictures/white.png",
    gamefield.DiskType.NONE: "pictures/empty.png",
}


class Field(QGridLayout):
    def __init__(self, widget, game_driver, *__args):
        super().__init__(*__args)
        self._game_driver = game_driver
        self._field_data = self._game_driver.game.field
        self._set_field()

    def _set_field(self):
        for y in range(self._field_data.side_length):
            for x in range(self._field_data.side_length):
                label = QLabel()
                pixmap = QPixmap(PICTURE_FROM_CELLSTATE[self._field_data[x][y]])
                label.setPixmap(pixmap)
                self.addWidget(label)


class ReversiWindow(QMainWindow):
    def __init__(self, game_driver):
        super().__init__()
        self._game_driver = game_driver
        self.setWindowTitle("Reversi")
        self.resize(500, 600)
        self._canvas = QImage()

        self._init_game_field()
        self.show()

    def _init_game_field(self):
        self._game_field = Field(self, self._game_driver)
        self._game_field.setParent(self)
        self._game_field.setGeometry(QRect(0, 100, 500, 600))


def start_app(game_driver):
    app = QApplication([])
    main_window = ReversiWindow(game_driver)
    sys.exit(app.exec_())


def parse_args():
    pass


def main():
    args = parse_args()
    game_driver = driver.GameDriver()
    start_app(game_driver)


if __name__ == "__main__":
    main()
