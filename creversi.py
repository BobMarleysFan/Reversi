import os
from gamefield import CellState, Field
import sys
from game import GameState
from driver import GameDriver

CELL_PRINTER = {
    CellState.EMPTY: '.',
    CellState.WHITE: '@',
    CellState.BLACK: 'O'
}


def print_field(game_state):
    for y in range(game_state.field.side_length):
        for x in range(game_state.field.side_length):
            print(CELL_PRINTER[game_state.field[x][y]], end='')
        print()


class Commands:
    def __init__(self, driver):
        if not isinstance(driver, GameDriver):
            raise TypeError
        self._driver = driver

    @property
    def game_state(self):
        return self._driver.game

    def cmd_place_disk(self, *coords):
        if not self._driver.game.make_move((int(coords[0]), int(coords[1]))):
            print("Недопустимый ход!")
        else:
            check_end_game(self._driver.game)
            if not self._driver.game.is_pvp:
                self._driver.game.make_computer_move()
            print_field(self._driver.game)
            check_end_game(self._driver.game)

    def cmd_show(self):
        print_field(self._driver.game)

    def cmd_help(self):
        print("Доступные команды:")
        print("new [size] ['pvp'/'pve']")
        print("place [x] [y]")
        print("show")
        print("exit")

    def cmd_new_game(self, side_length=8, pvp=False):
        if str.lower(str(pvp)) == "pvp":
            pvp = True
        elif str.lower(str(pvp)) == "pve":
            pvp = False
        elif pvp:
            raise ValueError()
        self._driver.new_game(int(side_length), pvp)
        print_field(self._driver.game)

    def cmd_exit(self):
        sys.exit()


def parse_args():
    pass


def main():
    args = parse_args()
    start_game()


def start_game():
    executor = Commands(GameDriver())
    while True:
        read_command(executor)


def read_command(executor):
    print("Ходят {}...".format("белые" if executor.game_state.current_player == CellState.WHITE
                               else "чёрные"))
    command = input("Введите команду: ").strip().split()
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
        print("Неверная команда!")


def check_end_game(game_state):
    if not game_state.get_move(0, 0):
        end_game(game_state)


# TODO: Обработка завершения игры
def end_game(game_state):
    print("Игра окончена. ", end="")
    if game_state.white_count > game_state.black_count:
        print("Победили белые!")
    elif game_state.black_count > game_state.white_count:
        print("Победили чёрные!")
    else:
        print("Ничья!")


if __name__ == "__main__":
    main()
