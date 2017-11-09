import unittest
import sys

sys.path.append(r"C:\Users\MK\PycharmProjects\Reversi")

from reversi import driver, game, gamefield


class MyTestCase(unittest.TestCase):
    def test_default_driver(self):
        game_driver = driver.GameDriver()
        pass


if __name__ == '__main__':
    unittest.main()
