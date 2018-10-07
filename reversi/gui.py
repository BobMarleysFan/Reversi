from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QIcon, QColor, QPainter, QPixmap, QBrush
from PyQt5.QtWidgets import QGridLayout, QWidget, QMainWindow, QPushButton

from reversi import gamefield


class ReversiWindow(QMainWindow):
    def __init__(self, driver, parent=None):
        super().__init__(parent)
        self._cell_size = 36
        self._field_widget = FieldWidget(driver, self._cell_size, parent=self)

        self._score_widget = ScoreWidget(driver.game.black_count, driver.game.white_count)
        self._score_widget_height = 32
        self._score_widget.setFixedHeight(self._score_widget_height)
        self._driver = driver

        _layout = QGridLayout()
        _layout.setSpacing(0)
        _layout.addWidget(self._score_widget, 0, 0)
        _layout.addWidget(self._field_widget, 1, 0)

        _window = QWidget()
        _window.setLayout(_layout)

        self.setCentralWidget(_window)

        self.setMinimumSize(self._cell_size * driver.game.field.side_length + 20,
                            self._cell_size * driver.game.field.side_length + 20 + self._score_widget_height)
        self.setWindowTitle("Reversi")


class ScoreWidget(QWidget):
    def __init__(self, black_count, white_count, parent=None):
        super().__init__(parent)
        self.black_count = black_count
        self.white_count = white_count

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        _white_color = QColor(255, 255, 255)
        _black_color = QColor(0, 0, 0)
        _height = self.geometry().height()
        _width = self.geometry().width()

        self.draw_player_score(painter,
                               QIcon(r".\pictures\black.png"),
                               _white_color,
                               self.black_count,
                               QRect(0, 0, int(_width / 2), _height))
        self.draw_player_score(painter,
                               QIcon(r".\pictures\white.png"),
                               _black_color,
                               self.white_count,
                               QRect(int(_width/2), 0, int(_width/2), _height))

    def draw_player_score(self, painter, player_icon, background_color, score, rect):
        painter.setBrush(QBrush(background_color))
        painter.setPen(background_color)
        painter.drawRect(rect)
        player_icon.paint(painter, rect)
        painter.drawText(QRect(100,10,50,50), Qt.AlignRight, ":" + str(score))

class FieldWidget(QWidget):
    def __init__(self, driver, cell_size=36, parent=None):
        super().__init__(parent)
        self.cell_size = cell_size
        self._driver = driver
        self._field = driver.game.field

    def paintEvent(self, q_paint_event):
        painter = QPainter(self)
        for x in range(self._field.side_length):
            for y in range(self._field.side_length):
                painter.save()
                self.draw_cell(painter, x, y)
                _grid_cell = QRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                painter.drawRect(_grid_cell)
                painter.restore()

    def draw_cell(self, painter, x, y):
        rect = self.get_rect_from_coords(x, y)
        value = self._field[x][y]
        background_tile_icon = QIcon(r".\pictures\background.png")
        background_tile_icon.paint(painter, rect)
        if value != gamefield.DiskType.NONE:
            disk_icon = self.get_disk_icon_from_type(value)
            if disk_icon is not None:
                disk_icon.paint(painter, rect)

    def get_rect_from_coords(self, x, y):
        return QRect(x * self.cell_size, y * self.cell_size,
                     self.cell_size, self.cell_size)

    @staticmethod
    def get_disk_icon_from_type(value):
        filename_from_type = {
            gamefield.DiskType.BLACK: r".\pictures\black.png",
            gamefield.DiskType.WHITE: r".\pictures\white.png"
        }
        return QIcon(filename_from_type[value])

    def mouseReleaseEvent(self, QMouseEvent):
        release_pos = QMouseEvent.pos()
        coords = [int(release_pos.x() / self.cell_size), int(release_pos.y() / self.cell_size)]
        self._driver.try_make_turn(coords)
        self.repaint()
