"""
Unit Tests for the GAC framework
"""

import unittest

from boards import TwoDimensionalBoard
from exceptions import InvalidCoordinatesException

class TestBoards(unittest.TestCase):
    """ Test Case for testing the board classes """

    def test_2d_board(self):
        """ Tests the TwoDimensionalBoard class """
        # Assume creating a board with negative dimensions will fail
        with self.assertRaises(ValueError):
            TwoDimensionalBoard(-5, 0)

        # Create a new 10x10 board and fill slot 5x5 with the letter 'a'
        board = TwoDimensionalBoard(10, 10)
        board.set(5, 5, 'a')

        # Assume we can get data from the board
        self.assertTrue(board.is_available(0, 0))
        self.assertEqual(board.get(5, 1), None)
        self.assertEqual(board.get(5, 5), 'a')

        # Assume an exception when fetching data at locations that do not match the board size
        with self.assertRaises(InvalidCoordinatesException):
            board.get(100, 100)
            board.get(-5, 0)

if __name__ == '__main__':
    unittest.main()
