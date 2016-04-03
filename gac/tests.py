"""
Unit Tests for the GAC framework
"""

import unittest

from boards import TwoDimensionalBoard
from client import OutgoingCommand, IncomingCommand
from exceptions import InvalidCoordinatesException
from games import Game


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


class TestGames(unittest.TestCase):
    """ Test Case for the various game implementation classes """

    def test_base_game(self):
        """ Tests functionality of the base game class """

        # This is a mock class - we'll use it to test the Game class
        class TestGameMock(Game):
            turn_ok = False

            def next_turn(self):
                if self.is_playing:
                    self.turn_ok = True
                self.is_playing = False

        # Create a new instance of the TestGameMock class and play it
        game = TestGameMock()
        game.play()

        # Now assume we got round to actually being able to play
        self.assertTrue(game.turn_ok)


class TestClient(unittest.TestCase):
    """ Test Case for the client classes """

    def test_commands(self):
        """ Tests constructing and parsing commands """
        # Test constructing commands to be sent to the server
        cmd = OutgoingCommand('UT')
        self.assertEqual(str(cmd), 'UT')
        self.assertEqual(cmd.command, 'UT')
        self.assertIsNone(cmd.arguments)
        self.assertFalse(cmd.has_arguments)

        cmd = OutgoingCommand('UT', 'GAME', ['example1', 'example2'])
        self.assertEqual(str(cmd), 'UT GAME ["example1", "example2"]')
        self.assertEqual(cmd.command, 'UT')
        self.assertEqual(cmd.arguments, ('GAME', ['example1', 'example2']))
        self.assertTrue(cmd.has_arguments)

        # Test parsing commands from the server
        cmd = IncomingCommand('UT')
        self.assertEqual(str(cmd), 'UT')
        self.assertEqual(cmd.command, 'UT')
        self.assertIsNone(cmd.arguments)
        self.assertFalse(cmd.has_arguments)

        cmd = IncomingCommand('UT GAME ["example1", "example2"]')
        self.assertEqual(str(cmd), 'UT GAME ["example1", "example2"]')
        self.assertEqual(cmd.command, 'UT')
        self.assertEqual(cmd.arguments[0], 'GAME')
        self.assertEqual(cmd.arguments[1], ['example1', 'example2'])
        self.assertTrue(cmd.has_arguments)


if __name__ == '__main__':
    unittest.main()