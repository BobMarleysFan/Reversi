import os
import sys
import argparse
from reversi import gamefield, driver
from reversi.gamefield import DiskType
import re

CELL_PRINTER = {
    gamefield.DiskType.NONE: '.',
    gamefield.DiskType.WHITE: '@',
    gamefield.DiskType.BLACK: 'O'
}

MODE_RE = re.compile('[pe]v[pe]')


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
        return self._driver.game

    def cmd_place_disk(self, *coords):
        if not self._driver.game.make_move((int(coords[0]) - 1, int(coords[1]) - 1)):
            print("Invalid move!")
        else:
            if self.game_state.check_end_game():
                end_game(self.game_state)
            if self._driver.game.mode == "pve":
                self._driver.game.make_computer_move()
            print_info(self._driver.game)

    def cmd_show(self):
        print_info(self._driver.game)

    def cmd_help(self):
        print("Available commands:")
        print("new <size> ['pvp'/'pve'/'evp'/'eve']")
        print("place <x> <y>")
        print("show")
        print("exit")

    def cmd_new_game(self, side_length=8, mode="pve"):
        if re.fullmatch(MODE_RE, str.lower(mode)):
            mode = str.lower(mode)
        else:
            raise ValueError("Wrong game mode: {}!".format(mode))
        self._driver.new_game(int(side_length), mode)

    def cmd_exit(self):
        sys.exit()


def parse_args():
    pass


def main():
    args = parse_args()
    start_game()


def start_game():
    executor = Commands(driver.GameDriver())
    while True:
        try:
            if not executor.game_state.game_over:
                if executor.game_state.check_end_game():
                    end_game(executor.game_state)
                if executor.game_state.mode == "evp" \
                        and executor.game_state.current_player == DiskType.BLACK:
                    executor.game_state.make_computer_move()
                    print_info(executor.game_state)
                elif executor.game_state.mode == "eve":
                    executor.game_state.make_computer_move()
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
        "exit": executor.cmd_exit
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
    elif game_state.black_count > game_state.white_count:
        print("Black won!")
    else:
        print("Draw!")
    sys.exit()


if __name__ == "__main__":
    main()
