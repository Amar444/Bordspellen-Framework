"""
Provides implementation for Player objects
"""


class Player(object):
    """ Player is used to define a player in the game """

    game = None

    def __init__(self, game):
        self.game = game

    def play(self):
        """ It is your turn, play the game """
        pass


class BoardPlayerMixin(Player):
    """ Player mixin that supports having a board """

    board = None
    print_board = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = self.game.board

    def play(self):
        """ Prints the board to the console while playing if enabled """
        if self.print_board:
            print(self.board)
        super().play()


class NamedPlayerMixin(Player):
    """ Player mixin that supports having a name """

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name or 'Unknown'

    def play(self):
        """ It is your turn, play the game """
        print(self.name, "is now playing.")
        super().play()

    def __str__(self):
        """ Returns the current player name """
        return self.name


class ClientPlayerMixin(Player):
    """ Player mixin that supports having a client associated with it """

    client = None

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
