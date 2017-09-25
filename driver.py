from game import GameState
from gamefield import Field, CellState


class GameDriver:
    def __init__(self, field=Field(), pvp=False):
        self._game_state = GameState(field, CellState.BLACK, pvp)

    def new_game(self, field_side_length=8, is_pvp=False):
        self._game_state = GameState(Field(field_side_length), CellState.BLACK, is_pvp)

    @property
    def game(self):
        return self._game_state
