"""
Unit Tests for the TicTacToe implementation
"""

import unittest
from game import TicTacToeGame
from players import Player, BoardPlayerMixin, NamedPlayerMixin


class TestPlayer(NamedPlayerMixin, BoardPlayerMixin, Player):
    """ Create player to test with """
    def play(self):
        super().play()


class TestTicTacToe(unittest.TestCase):
    """ Test TicTacToe """
    game = TicTacToeGame()
    players = (TestPlayer(name="X", board=game.board),)
    players += (TestPlayer(name="O", board=game.board),)

    game.set_players(players)

    def test_win_horizontal(self):
        """ Test winning horizontal """
        self.game.board.set(0, 0, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(0, 2, self.players[0])
        self.game.board.set(2, 0, self.players[1])
        self.game.board.set(0, 1, self.players[0])

        self.assertEqual(self.game.has_won_horizontal(self.players[0]), True)

        self.game.board.clear()

    def test_win_vertical(self):
        """ Test winning vertical """
        self.game.board.set(0, 1, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(2, 1, self.players[0])
        self.game.board.set(2, 0, self.players[1])
        self.game.board.set(1, 1, self.players[0])

        self.assertEqual(self.game.has_won_vertical(self.players[0]), True)

        self.game.board.clear()

    def test_win_diagonal1(self):
        """ Test winning diagonal / """
        self.game.board.set(2, 0, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(0, 2, self.players[0])
        self.game.board.set(2, 2, self.players[1])
        self.game.board.set(1, 1, self.players[0])

        self.assertEqual(self.game.has_won_diagonal(self.players[0]), True)

        self.game.board.clear()

    def test_win_diagonal2(self):
        """ Test winning diagonal \ """
        self.game.board.set(0, 0, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(2, 2, self.players[0])
        self.game.board.set(2, 0, self.players[1])
        self.game.board.set(1, 1, self.players[0])

        self.assertEqual(self.game.has_won_diagonal(self.players[0]), True)

        self.game.board.clear()

    def test_state(self):
        """ Test state of the game """
        self.game.board.set(0, 0, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(2, 2, self.players[0])
        self.game.board.set(2, 0, self.players[1])
        self.game.board.set(1, 1, self.players[0])

        self.assertEqual(self.game.state, (1, self.players[0]))

        self.game.board.clear()

if __name__ == '__main__':
    unittest.main()
