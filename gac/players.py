"""
Provides implementation for Player objects
"""


class Player(object):
    """ Player is used to define a player in the game """

    def play(self):
        """ It is your turn, play the game """
        pass


class BoardPlayerMixin(Player):
    """ Player mixin that supports having a board """

    board = None
    print_board = True

    def __init__(self, board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board

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
    """ Player mixin that supports input from a server """

    client = None
    lastMove = None

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        client.on("SRV", self.handle_move)

    def handle_command(self, command):
        """ handles a command passed from the client, handling needs to be specified by siblings of this class """
        pass
