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
    def side_length(self):
        return self._side_length

    def __getitem__(self, item):
        return self._field[item]

    def check_coords(self, coords):
        if len(coords) != 2:
            return False
        return coords[0] < self._side_length and coords[1] < self._side_length \
            and self._field[coords[0]][coords[1]] == CellState.EMPTY

    def get_flip_instructions(self, coords, disk_color):
        """Возвращает список инструкций вида "(направление, количество)" для переворачивания фишек."""
        opponent_color = CellState(int(not disk_color.value))
        instructions = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                mult = 1
                disks_to_flip_count = 0
                new_x = dx * mult + coords[0]
                new_y = dy * mult + coords[1]
                while 0 <= new_x < self.side_length \
                        and 0 <= new_y < self.side_length \
                        and not (dx == 0 and dy == 0):
                    if self._field[new_x][new_y] == opponent_color:
                        disks_to_flip_count += 1
                        mult += 1
                        new_x = dx * mult + coords[0]
                        new_y = dy * mult + coords[1]
                    elif self._field[new_x][new_y] == disk_color and disks_to_flip_count > 0:
                        instructions.append((dx, dy, disks_to_flip_count))
                        break
                    else:
                        break
        return instructions


class CellState(Enum):
    WHITE = 0
    BLACK = 1
    EMPTY = 2
