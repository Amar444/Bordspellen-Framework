"""
Games
"""

from .boards import Board
from exceptions import *

class Game(object):
    """ Provides you with the tools to set up a game """

    is_playing = False
    players = ()

    def play(self):
        """ Starts playing the game until `is_playing` is set to False """
        self.is_playing = True

    def set_players(self, players: tuple):
        """ Adds the given players to the game """
        self.players = players


class TurnBasedGame(Game):
    """
    Mixin for games that allows for handling turn-based games. You will be allowed to add
    players to the game, which will be able to play the game on a turn-by-turn basis.
    """

    current_turn = 0

    def play(self):
        super().play()
        while self.is_playing:
            self.next_turn()

    def next_turn(self):
        """ Plays the next turn in the game """
        self.players[self.current_turn].play()
        self.current_turn = 0 if self.current_turn == len(self.players) - 1 else self.current_turn + 1


class BoardGame(Game):
    """ Mixin for games that allows for basic handling of a Board """

    board = None
    board_class = None

    def __init__(self, *args, **kwargs):
        """ Initializes a new game and sets up the board class """
        super().__init__(*args, **kwargs)
        if self.board_class is not None and issubclass(self.board_class, Board):
            self.board = self.board_class()

    def play(self):
        if self.board is None:
            raise InvalidBoardException()

        super().play()
