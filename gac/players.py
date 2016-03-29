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

    name = 'Unknown'

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def play(self):
        """ It is your turn, play the game """
        print(self.name, "is now playing.")
        super().play()
