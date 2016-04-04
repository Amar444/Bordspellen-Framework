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



class CommandLineInputPlayerMixin(Player):
    """ Player mixin that supports input from the command line """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self):
        """ Asks for input and places the input on the board.
        If the input is not valid the exception will be printed and this method gets called again."""
        try:
            coords = input("Please enter coords to update the board? [x,y] ")
            x, y = coords.split(',')
            self.board.set(int(x), int(y), self.name[0:1])
            print("\n")
        except Exception as e:
            print(e)
            self.play()

    def __str__(self):
        """ Returns the current player name """
        return self.name

