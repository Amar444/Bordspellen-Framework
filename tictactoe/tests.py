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

    def test_state(self):
        """ Test state of the game """
        self.game.board.set(0, 0, self.players[0])
        self.game.board.set(1, 2, self.players[1])
        self.game.board.set(2, 2, self.players[0])
        self.game.board.set(2, 0, self.players[1])
        self.game.board.set(1, 1, self.players[0])

        self.assertEqual(self.game.state, (1, self.players[0]))

if __name__ == '__main__':
    unittest.main()
