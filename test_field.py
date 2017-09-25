import unittest
from gamefield import Field, CellState


class TestField(unittest.TestCase):
    def test_indexer(self):
        field = Field(4)
        self.assertEqual(field[0], [CellState.EMPTY]*4)
        self.assertEqual(field[1][1], CellState.WHITE)

    def test_default_field(self):
        field = Field()
        self.assertEqual(field.side_length, 8)
        self.assertEqual(field[0][0], CellState.EMPTY)
        self.assertEqual(field[3][3], CellState.WHITE)
        self.assertEqual(field[4][3], CellState.BLACK)
        self.assertEqual(field[7][6], CellState.EMPTY)
        
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


if __name__ == "__main__":
    unittest.main()
