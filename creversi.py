import argparse
import logging
import re
import sys

from reversi import gamefield, driver
from reversi.gamefield import DiskType

LOGGER = logging.getLogger("creversi")

CELL_PRINTER = {
    gamefield.DiskType.NONE: '.',
    gamefield.DiskType.WHITE: '@',
    gamefield.DiskType.BLACK: 'O'
}

MODE_RE = re.compile('[pe]v[pe]')

__author__ = "Alexander Sanochkin"


def print_field(game_state):
    for y in range(game_state.field.side_length):
        for x in range(game_state.field.side_length):
            print(CELL_PRINTER[game_state.field[x][y]], end='')
        print()


def print_info(game_state):
    print_field(game_state)
    print("White: {}. Black: {}.".format(
        game_state.white_count, game_state.black_count))
    print("Current turn: {}".format(
        "black" if game_state.current_player == DiskType.BLACK else "white"))


class Commands:
    def __init__(self, game_driver):
        if not isinstance(game_driver, driver.GameDriver):
            raise TypeError
        self._driver = game_driver

    @property
    def game_state(self):
        return self.driver.game

    @property
    def driver(self):
        return self._driver

    def cmd_place_disk(self, *coords):
        if not self.driver.make_turn((int(coords[0]) - 1, int(coords[1]) - 1)):
            print("Invalid move!")
        else:
            if self.game_state.check_end_game():
                end_game(self.game_state)
            if self.driver.game.mode == "pve":
                self.driver.make_computer_turn()
            print_info(self.driver.game)

    def cmd_show(self):
        print_info(self.driver.game)

    def cmd_help(self):
        print("Available commands:")
        print("new <size> ['pvp'/'pve'/'evp'/'eve']")
        print("place <x> <y>")
        print("show")
        print("save [file name]")
        print("load [file name]")
        print("undo")
        print("redo")
        print("moves")
        print("exit")

    def cmd_new_game(self, side_length=8, mode="pve"):
        if re.fullmatch(MODE_RE, str.lower(mode)):
            mode = str.lower(mode)
        else:
            raise ValueError("Wrong game mode: {}!".format(mode))
        self.driver.new_game(int(side_length), mode)

    def cmd_save(self, save_name="new_save"):
        self.driver.save_game(save_name)

    def cmd_load(self, load_name="new_save"):
        self._driver = self.driver.load_game(load_name)

    def cmd_undo(self):
        self.driver.undo_turn()

    def cmd_redo(self):
        self.driver.redo_turn()

    def cmd_show_turns(self):
        LOGGER.info("Showing available moves.")
        possible_turns = []
        side = self.game_state.field.side_length
        turn = self.game_state.get_turn()
        while turn:
            possible_turns.append(turn[0])
            turn = self.game_state.get_turn(turn[0][0] + 1, turn[0][1])
        for y in range(side):
            for x in range(side):
                if (x, y) in possible_turns:
                    print('*', end='')
                else:
                    print(CELL_PRINTER[self.game_state.field[x][y]], end='')
            print()

    def cmd_exit(self):
        LOGGER.info("Exiting game.")
        sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(description="Console version of Reversi.",
                                     epilog="Author: {}".format(__author__))
    parser.add_argument("-n", "--new", help="new game", nargs=2, metavar=("side", "mode"))
    parser.add_argument("-l", "--load", help="load game", type=str, metavar="filename")
    return parser.parse_args()


def main():
    args = parse_args()
    logger = logging.getLogger("creversi")
    logging.basicConfig(filename="creversi.log", level=logging.INFO)
    if args.new:
        start_game(Commands(driver.GameDriver(
            field=gamefield.Field(side_length=int(args.new[0])),
            mode=args.new[1])))
    if args.load:
        start_game(Commands(driver.GameDriver.load_game(args.load[0])))
    start_game()


def start_game(executor=None):
    if executor is None:
        executor = Commands(driver.GameDriver())
    while True:
        try:
            if not executor.game_state.game_over:
                if executor.game_state.check_end_game():
                    end_game(executor.game_state)
                if executor.game_state.mode == "evp" \
                        and executor.game_state.current_player == DiskType.BLACK:
                    executor.driver.make_computer_turn()
                    print_info(executor.game_state)
                elif executor.game_state.mode == "eve":
                    executor.driver.make_computer_turn()
                    print_info(executor.game_state)
                    continue
            read_command(executor)
        except Exception as e:
            print()
            print(e, file=sys.stderr)


def read_command(executor):
    command = input("Enter a command: ").strip().split()
    execute_command(executor, *command)


def execute_command(executor, command, *args):
    commands = {
        "new": executor.cmd_new_game,
        "place": executor.cmd_place_disk,
        "show": executor.cmd_show,
        "help": executor.cmd_help,
        "exit": executor.cmd_exit,
        "save": executor.cmd_save,
        "load": executor.cmd_load,
        "undo": executor.cmd_undo,
        "redo": executor.cmd_redo,
        "moves": executor.cmd_show_turns
    }
    if command in commands:
        commands[command](*args)
    else:
        raise ValueError("Wrong command!")


def end_game(game_state):
    print_field(game_state)
    print("White: {}. Black: {}.".format(
        game_state.white_count, game_state.black_count))
    print("Game Over. ", end="")
    if game_state.white_count > game_state.black_count:
        print("White won!")
        LOGGER.info("White won.")
    elif game_state.black_count > game_state.white_count:
        print("Black won!")
        LOGGER.info("Black won.")
    else:
        print("Draw!")
        LOGGER.info("Draw.")
    sys.exit()


if __name__ == "__main__":
    main()
