from enum import Enum


class Field:
    def __init__(self, side_length=8, cells=None):
        if side_length % 2 == 1:
            raise ValueError("Field side length must be an even number")
        if side_length < 3:
            raise ValueError("Field side length must be greater than 3")
        self._side_length = side_length
        if cells is None:
            self._field = [[DiskType.NONE] * side_length for i in range(side_length)]
            half_side_length = side_length // 2
            self._field[half_side_length - 1][half_side_length - 1] = DiskType.WHITE
            self._field[half_side_length][half_side_length] = DiskType.WHITE
            self._field[half_side_length - 1][half_side_length] = DiskType.BLACK
            self._field[half_side_length][half_side_length - 1] = DiskType.BLACK
        else:
            self._field = cells

    @property
    def side_length(self):
        return self._side_length

    def __getitem__(self, item):
        return self._field[item]

    def check_coords(self, coords):
        if len(coords) != 2:
            return False
        return coords[0] < self._side_length and coords[1] < self._side_length \
               and self._field[coords[0]][coords[1]] == DiskType.NONE

    def get_flip_instructions(self, coords, disk_color):
        """Возвращает список инструкций вида "(направление, количество)" для переворачивания фишек."""
        opponent_color = DiskType(int(not disk_color.value))
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

    def get_disks_count_by_color(self, color):
        disks_count = 0
        for row in self._field:
            for cell in row:
                if cell == color:
                    disks_count += 1
        return disks_count

    def get_white_disks_count(self):
        return self.get_disks_count_by_color(DiskType.WHITE)

    def get_black_disks_count(self):
        return self.get_disks_count_by_color(DiskType.BLACK)

    def __str__(self):
        return ":".join("".join(list(map(lambda disk: str(disk.value),
                                         self._field[x]))) for x in range(self._side_length))

    @staticmethod
    def from_string(string):
        columns = string.strip("\n").split(":")
        field = []
        for column in columns:
            if len(column) == len(columns):
                field.append(list(map(lambda value: DiskType(int(value)), column)))
            else:
                raise ValueError("Given string is not a field representation.")
        return Field(len(columns), field)


class DiskType(Enum):
    WHITE = 0
    BLACK = 1
    NONE = 2
    COMMON = 3

    def __str__(self):
        return str.lower(self.name)

    @staticmethod
    def get_opposite_type(type):
        if type == DiskType.NONE or type == DiskType.COMMON:
            return type
        return DiskType.BLACK if type == DiskType.WHITE else DiskType.WHITE
