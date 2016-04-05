"""
Unit Tests for the TicTacToe implementation
"""

import unittest
from game import TicTacToeGame, STATUS_WINNER, STATUS_UNCLEAR, STATUS_DRAW
from players import Player, BoardPlayerMixin, NamedPlayerMixin


class TestPlayer(NamedPlayerMixin, BoardPlayerMixin, Player):
    """ Create player to test with """
    def play(self):
        super().play()


class TestTicTacToe(unittest.TestCase):
    """ Test TicTacToe """

    game = None
    p1 = None
    p2 = None

    def __init__(self, *args, **kwargs):
        """ Sets up the tests """
        super().__init__(*args, **kwargs)

        self.game = TicTacToeGame()

        self.p1 = TestPlayer(name="X", board=self.game.board)
        self.p2 = TestPlayer(name="O", board=self.game.board)

        self.game.set_players((self.p1, self.p2))

    def tearDown(self):
        """ Clears the board after each individual test """
        self.game.board.clear()

    def test_win_horizontal(self):
        """ Test winning horizontal """
        self.game.board.set(0, 0, self.p1)
        self.game.board.set(1, 2, self.p2)
        self.game.board.set(0, 2, self.p1)
        self.game.board.set(2, 0, self.p2)
        self.game.board.set(0, 1, self.p1)

        self.assertEqual(self.game.has_won_horizontal(self.p1), True)

    def test_win_vertical(self):
        """ Test winning vertical """
        self.game.board.set(0, 1, self.p1)
        self.game.board.set(1, 2, self.p2)
        self.game.board.set(2, 1, self.p1)
        self.game.board.set(2, 0, self.p2)
        self.game.board.set(1, 1, self.p1)

        self.assertEqual(self.game.has_won_vertical(self.p1), True)

    def test_win_diagonal1(self):
        """ Test winning diagonal / """
        self.game.board.set(2, 0, self.p1)
        self.game.board.set(1, 2, self.p2)
        self.game.board.set(0, 2, self.p1)
        self.game.board.set(2, 2, self.p2)
        self.game.board.set(1, 1, self.p1)

        self.assertEqual(self.game.has_won_diagonal(self.p1), True)

    def test_win_diagonal2(self):
        """ Test winning diagonal \ """
        self.game.board.set(0, 0, self.p1)
        self.game.board.set(1, 2, self.p2)
        self.game.board.set(2, 2, self.p1)
        self.game.board.set(2, 0, self.p2)
        self.game.board.set(1, 1, self.p1)

        self.assertEqual(self.game.has_won_diagonal(self.p1), True)

    def test_draw(self):
        """ Test draw """
        self.game.board.set(0, 0, self.p1)
        self.game.board.set(0, 1, self.p2)
        self.game.board.set(1, 1, self.p1)
        self.game.board.set(0, 2, self.p2)
        self.game.board.set(1, 2, self.p1)
        self.game.board.set(1, 0, self.p2)
        self.game.board.set(2, 0, self.p1)
        self.game.board.set(2, 2, self.p2)
        self.game.board.set(2, 1, self.p1)

        self.assertEqual(self.game.state, (STATUS_DRAW, None))

    def test_state(self):
        """ Test state of the game """
        self.assertEqual(self.game.state, (STATUS_UNCLEAR, None))

        self.game.board.set(0, 0, self.p1)
        self.game.board.set(1, 2, self.p2)
        self.game.board.set(2, 2, self.p1)
        self.game.board.set(2, 0, self.p2)
        self.game.board.set(1, 1, self.p1)

        self.assertEqual(self.game.state, (STATUS_WINNER, self.p1))

if __name__ == '__main__':
    unittest.main()
