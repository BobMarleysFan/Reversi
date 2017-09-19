from gamefield import Field, CellState
import datetime

CELL_PRINTER = {
    CellState.EMPTY: ' ',
    CellState.WHITE: '@',
    CellState.BLACK: 'O'
}


class GameState:
    def __init__(self, field):
        self._field = field
        self._white_count = 2
        self._black_count = 2
        self._game_start_time = datetime.datetime.now()

    def print_field(self):
        print(' ' + ''.join(str(i + 1) for i in range(self._field.side_length)))
        for y in range(self._field.side_length):
            print(y + 1, end='')
            for x in range(self._field.side_length):
                print(CELL_PRINTER[self._field.field[x][y]], end='')
            print()

    def make_turn(self, coords, is_players_turn=True):
        chips_color = CellState.BLACK if is_players_turn else CellState.WHITE
        if not self._field.check_coords(coords):
            return False
        inverting_instructions = self._field.get_inverting_instructions(coords, is_players_turn)
        if inverting_instructions:
            self._field.field[coords[0]][coords[1]] = chips_color
            for instruction in inverting_instructions:
                for i in range(instruction[2]):
                    new_x = coords[0] + instruction[0] * (i + 1)
                    new_y = coords[1] + instruction[1] * (i + 1)
                    self._field.field[new_x][new_y] = chips_color
            return True
        return False
