import os
import unittest
import sys

sys.path.append(r"C:\Users\MK\PycharmProjects\Reversi")
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
#                              os.path.pardir))

from reversi.gamefield import Field, DiskType


class TestField(unittest.TestCase):
    def test_indexer(self):
        field = Field(4)
        self.assertEqual(field[0], [DiskType.NONE] * 4)
        self.assertEqual(field[1][1], DiskType.WHITE)

    def test_default_field(self):
        field = Field()
        self.assertEqual(field.side_length, 8)
        self.assertEqual(field[0][0], DiskType.NONE)
        self.assertEqual(field[3][3], DiskType.WHITE)
        self.assertEqual(field[4][3], DiskType.BLACK)
        self.assertEqual(field[7][6], DiskType.NONE)

    def test_incorrect_parameters(self):
        with self.assertRaises(ValueError):
            Field(2)
        with self.assertRaises(ValueError):
            Field(9)

    def test_coords_checking(self):
        field = Field(4)
        self.assertEqual(field.check_coords((3,)), False)
        self.assertEqual(field.check_coords((3, 3)), True)
        self.assertEqual(field.check_coords((2, 1)), False)
        self.assertEqual(field.check_coords((5, 2)), False)

    def test_flip_instructions(self):
        field = Field(4)
        self.assertEqual(field.get_flip_instructions((1, 0), DiskType.BLACK), [(0, 1, 1)])
        self.assertEqual(field.get_flip_instructions((1, 0), DiskType.WHITE), [])
        self.assertEqual(field.get_flip_instructions((0, 0), DiskType.BLACK), [])


if __name__ == "__main__":
    unittest.main()
