import unittest
from gamefield import Field, CellState


class TestField(unittest.TestCase):
    def test_default_field(self):
        field = Field()
        self.assertEqual(field.field[0][0], CellState.EMPTY)
        self.assertEqual(field.field[3][3], CellState.WHITE)
        self.assertEqual(field.field[4][3], CellState.BLACK)
        self.assertEqual(field.field[7][6], CellState.EMPTY)
        #self.assertRaises(ValueError, Field.__init__(Field(), 9))


if __name__ == "__main__":
    unittest.main()
