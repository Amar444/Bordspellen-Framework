"""
Games
"""

from boards import Board
from exceptions import *

class Game(object):
    """ Provides you with the tools to set up a game """

    players = ()
    name = None
    is_playing = False

    controller = None
    controller_class = None

    def __init__(self, controller=None):
        if controller is None:
            self.controller = self.controller_class(self)
        else:
            self.controller = controller

    def set_players(self, players: tuple):
        """ Adds the given players to the game """
        self.players = players

    def play(self):
        """ Starts playing the game until `is_playing` is set to False """
        self.is_playing = True
        self.controller.play()


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


class GameController(object):
    pass


class TurnBasedGameController(GameController):
    current_turn = 0
    game = None

    def __init__(self, game):
        self.game = game

    def play(self):
        while self.game.is_playing:
            self.next_turn()

    def next_turn(self):
        """ Plays the next turn in the game """
        self.game.players[self.current_turn].play()
        self.current_turn = 0 if self.current_turn == len(self.game.players) - 1 else self.current_turn + 1
