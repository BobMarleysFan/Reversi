import sys
import unittest

sys.path.append(r"C:\Users\MK\PycharmProjects\Reversi")
from reversi.game import GameState
from reversi.gamefield import Field, DiskType


class TestGame(unittest.TestCase):
    def test_properties(self):
        field = Field(6)
        game = GameState(field, DiskType.WHITE, "pvp", 2, 2)
        self.assertEqual(game.field, field)
        self.assertEqual(game.current_player, DiskType.WHITE)
        self.assertEqual(game.white_count, 2)
        self.assertEqual(game.black_count, 2)
        self.assertEqual(game.mode, "pvp")

    def test_place_and_flip_disk(self):
        game = GameState(Field(4), DiskType.BLACK, "pve", 2, 2)
        game.place_or_flip_disk(1, 0)
        self.assertEqual([DiskType.BLACK, DiskType.WHITE, DiskType.BLACK, DiskType.NONE], game.field[1])
        game.place_or_flip_disk(1, 0)
        self.assertEqual([DiskType.BLACK, DiskType.WHITE, DiskType.BLACK, DiskType.NONE], game.field[1])
        game.place_or_flip_disk(1, 1)
        self.assertEqual([DiskType.BLACK, DiskType.BLACK, DiskType.BLACK, DiskType.NONE], game.field[1])
