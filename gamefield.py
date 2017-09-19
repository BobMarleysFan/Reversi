from enum import Enum


class Field:
    def __init__(self, side_length=8):
        if side_length % 2 == 1:
            raise ValueError("Field side length must be an even number")
        if side_length < 3:
            raise ValueError("Field side length must be greater than 3")
        self._side_length = side_length
        self._field = [[CellState.EMPTY] * side_length for i in range(side_length)]
        half_side_length = side_length // 2
        self._field[half_side_length - 1][half_side_length - 1] = CellState.WHITE
        self._field[half_side_length][half_side_length] = CellState.WHITE
        self._field[half_side_length - 1][half_side_length] = CellState.BLACK
        self._field[half_side_length][half_side_length - 1] = CellState.BLACK

    @property
    def field(self):
        return self._field

    @property
    def side_length(self):
        return self._side_length

    def check_coords(self, coords):
        if len(coords) != 2:
            return False
        return coords[0] < self._side_length and coords[1] < self._side_length \
            and self._field[coords[0]][coords[1]] == CellState.EMPTY

    def get_inverting_instructions(self, coords, is_players_turn):
        """"Возвращает список инструкций для инвертирования фишек в направлениях от клетки поля."""
        chip_to_place, opponents_chip = (CellState.BLACK, CellState.WHITE) \
            if is_players_turn else (CellState.WHITE, CellState.BLACK)
        instructions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                mult = 1
                chips_to_invert_count = 0
                while 0 <= dx*mult + coords[0] < self.side_length \
                    and 0 <= dy*mult + coords[0] < self.side_length \
                    and not (dx == 0 and dy == 0):
                        new_x = dx*mult+coords[0]
                        new_y = dy*mult+coords[1]
                        if self._field[new_x][new_y] == chip_to_place and chips_to_invert_count > 0:
                            instructions.append((dx, dy, chips_to_invert_count))
                            break
                        elif self._field[new_x][new_y] == opponents_chip:
                            chips_to_invert_count += 1
                        else:
                            break
                        mult += 1
        return instructions


class CellState(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

