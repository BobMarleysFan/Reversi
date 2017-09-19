import os
import gamefield
import sys
from game import GameState


def parse_args():
    pass


def main():
    parse_args()
    start_game()


def start_game():
    print("Введите команду: ", end='')
    while True:
        read_command()


def read_command():
    command = input("Введите команду: ")



if __name__=="__main__":
    main()