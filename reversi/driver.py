import copy
import logging
import random

from . import game, gamefield
import os

LOGGER = logging.getLogger("reversi.driver")


class LoadException(Exception):
    pass


class GameDriver:
    def __init__(self, field=gamefield.Field(),
                 current_player=gamefield.DiskType.BLACK,
                 mode="pve",
                 white_count=2,
                 black_count=2):
        LOGGER.info("Starting new game in {} mode.".format(mode))
        self._game_state = game.GameState(field,
                                          current_player,
                                          mode)
        self._states = []
        self._redo = []

    def new_game(self, field_side_length=8, mode="pve"):
        LOGGER.info("Starting new game in {} mode.".format(mode))
        self._game_state = game.GameState(gamefield.Field(field_side_length),
                                          gamefield.DiskType.BLACK,
                                          mode)
        self._states = []
        self._redo = []

    def save_game(self, save_name):
        if not os.path.exists("saves"):
            os.mkdir("saves")
        save_name = "saves/{}.revsave".format(save_name)
        LOGGER.info("Game saved as {}.".format(save_name))
        with open(save_name, 'w', encoding="utf-8") as f:
            game = self.game
            f.write(str(game.field) + "\n")
            f.write("w{} b{}".format(game.white_count, game.black_count) + "\n")
            f.write(game.mode + "\n")
            f.write("black" if game.current_player == gamefield.DiskType.BLACK else "white")

    @staticmethod
    def load_game(filename):
        filename = "saves/{}.revsave".format(filename)
        if not os.path.exists(filename):
            LOGGER.error("File {} not found".format(filename))
            raise LoadException("No save file found.")
        with open(filename, 'r', encoding="utf-8") as f:
            content = f.readlines()
            field = gamefield.Field.from_string(content[0])
            disks_count = content[1].split()
            white_count = int(disks_count[0][1:])
            black_count = int(disks_count[1][1:])
            mode = content[2].strip("\n")
            current_player = gamefield.DiskType.BLACK if content[3] == "black" else gamefield.DiskType.WHITE
        LOGGER.info("Loaded game {}.".format(filename))
        return GameDriver(field, current_player, mode, white_count, black_count)

    def try_make_turn(self, coords):
        state = copy.deepcopy(self._game_state)
        if self.game.make_turn(coords):
            LOGGER.info("Player placed {} disk on {} {}.".format(self._game_state.other_player,
                                                                 *coords))
            self._states.append(state)
            self._redo = []
            return True
        return False

    def make_computer_turn(self):
        possible_turns = []
        for y in range(self.game.field.side_length):
            for x in range(self.game.field.side_length):
                turn = self.game.get_turn(x, y)
                if turn:
                    possible_turns.append(turn)
        random_turn = possible_turns[random.randrange(len(possible_turns))]

        LOGGER.info("Computer placed {} disk on {} {}.".format(self._game_state.current_player,
                                                               *random_turn[0]))
        self.game.make_turn(*random_turn)

    def undo_turn(self):
        if self._states:
            LOGGER.info("Undo turn")
            self._redo.append(copy.deepcopy(self._game_state))
            self._game_state = self._states.pop()
        else:
            LOGGER.info("Can't undo turn.")

    def redo_turn(self):
        if self._redo:
            LOGGER.info("Redo turn")
            self._game_state = self._redo.pop()
        else:
            LOGGER.info("Can't redo turn.")

    @property
    def game(self):
        return self._game_state
