from . import gamefield
import datetime
import random
import logging

LOGGER = logging.getLogger("reversi.game")

class GameState:
    def __init__(self, field, current_player, mode):
        self._field = field
        self._current_player = current_player
        self._other_player = gamefield.DiskType(int(not self.current_player.value))
        self._mode = mode
        self._white_count = field.get_white_disks_count()
        self._black_count = field.get_black_disks_count()
        self._gameover = False

    @property
    def mode(self):
        return self._mode

    @property
    def field(self):
        return self._field

    @property
    def white_count(self):
        return self._white_count

    @property
    def black_count(self):
        return self._black_count

    @property
    def current_player(self):
        return self._current_player

    @property
    def other_player(self):
        return self._other_player

    @property
    def game_over(self):
        return self._gameover

    def make_turn(self, coords, flipping_instructions=None):
        """Пытается сделать ход по указанным координатам и возвращает True, если удалось сделать ход."""
        if not self._field.check_coords(coords):
            return False
        if flipping_instructions is None:
            flipping_instructions = self._field.get_flip_instructions(coords, self._current_player)
        if flipping_instructions:
            self.place_or_flip_disk(*coords)
            for instruction in flipping_instructions:
                for i in range(instruction[2]):
                    new_x = coords[0] + instruction[0] * (i + 1)
                    new_y = coords[1] + instruction[1] * (i + 1)
                    self.place_or_flip_disk(new_x, new_y)
            self._other_player = self.current_player
            self._current_player = gamefield.DiskType(int(not self._current_player.value))
            return True
        return False

    def place_or_flip_disk(self, *coords):
        if self.field[coords[0]][coords[1]] == gamefield.DiskType.NONE:
            if self._current_player == gamefield.DiskType.WHITE:
                self._white_count += 1
            else:
                self._black_count += 1
        else:
            if self._current_player == gamefield.DiskType.WHITE:
                self._white_count += 1
                self._black_count -= 1
            else:
                self._black_count += 1
                self._white_count -= 1
        self._field[coords[0]][coords[1]] = self._current_player

    def remove_disk(self, *coords):
        if not self.field[coords[0]][coords[1]] == gamefield.DiskType.NONE:
            if self.field[coords[0]][coords[1]] == gamefield.DiskType.WHITE:
                self._white_count -= 1
            else:
                self._black_count -= 1
        self.field[coords[0][coords[1]]] = gamefield.DiskType.NONE

    def get_turn(self, start_x=0, start_y=0):
        """Ищет ход у текущего игрока, и возвращает координаты
        первой подходящей клетки и инструкции для неё. Если ходов нет - возвращает None"""
        for y in range(start_y, self._field.side_length):
            for x in range(start_x, self._field.side_length):
                if self._field[x][y] == gamefield.DiskType.NONE:
                    instructions = self._field.get_flip_instructions((x, y), self.current_player)
                    if instructions:
                        return (x, y), instructions
            start_x = 0
        return None

    def check_end_game(self):
        """Возвращает True, если больше нет ходов, иначе - False"""
        if not self.get_turn():
            self._gameover = True
            return True
        return False
