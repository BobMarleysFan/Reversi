from gamefield import Field, CellState
import datetime
import random


class GameState:
    def __init__(self, field, current_player, pvp):
        self._field = field
        self._current_player = current_player
        self._is_pvp = pvp
        self._game_start_time = datetime.datetime.now()
        self._white_count, self._black_count = (2, 2)

    @property
    def is_pvp(self):
        return self._is_pvp

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

    def make_move(self, coords, flipping_instructions=None):
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
            self._current_player = CellState(int(not self._current_player.value))
            return True
        return False

    def place_or_flip_disk(self, *coords):
        if self.field[coords[0]][coords[1]] == CellState.EMPTY:
            if self._current_player == CellState.WHITE:
                self._white_count += 1
            else:
                self._black_count += 1
        else:
            if self._current_player == CellState.WHITE:
                self._white_count += 1
                self._black_count -= 1
            else:
                self._black_count += 1
                self._white_count -= 1
        self._field[coords[0]][coords[1]] = self._current_player

    def make_computer_move(self):
        possible_moves = []
        for y in range(self._field.side_length):
            for x in range(self._field.side_length):
                move = self.get_move(x, y)
                if move:
                    possible_moves.append(move)
        random_move = possible_moves[random.randrange(len(possible_moves))]
        self.make_move(*random_move)

    def get_move(self, start_x, start_y):
        """Ищет ход у игрока с заданным цветом, и возвращает координаты
        первой подходящей клетки и инструкции для неё. Если ходов нет - возвращает False"""
        for y in range(start_y, self._field.side_length):
            for x in range(start_x, self._field.side_length):
                if self._field[x][y] == CellState.EMPTY:
                    instructions = self._field.get_flip_instructions((x, y), self.current_player)
                    if instructions:
                        return (x, y), instructions
            start_x = 0
        return False
