from players import BoardPlayerMixin, NamedPlayerMixin, ExternalInputPlayerMixin

"""
Assembles and implements player classes for the TicTacToe game
NOTE: this is still very experimental not everything can be tested sine a lot of code used is still changing or missing
"""


class CommandLinePlayer(BoardPlayerMixin, NamedPlayerMixin):
    """
    TicTacToe player that gives input from the command line and also
    receives information from the command line
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self):
        """ This player needs to make a move """
        super().play()

        try:
            coords = input("Please enter coords to update the board? [x,y] ")
            x, y = coords.split(',')
            self.board.set(int(x), int(y), self.name[0:1])
            print("\n")
        except Exception as e:
            print(e)
            self.play()


class ExternalInputPlayer(BoardPlayerMixin, NamedPlayerMixin, ExternalInputPlayerMixin):
    """
    TicTacToe player that receives input from a server
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def play(self):
        """ This player needs to make a move """
        super().play()

        # loop/wait until we got a move from the server
        # todo: make this work... Because it is in a loop it cannot do handle_move and thus never end the loop.
        while True:
            if self.lastMove is not None:
                x = self.lastMove.x
                y = self.lastMove.y
                x, y = None
                break

        try:
            self.board.set(int(x), int(y), self.name[0:1])
        except Exception as e:
            print(e)
            print("\n")
            """
            A move send from the server can't be invalid, this means we are wrong!
            No way to let the server know you are do not agree with the move.
            """
            raise ExplosionWithFireException()

    def handle_move(self, move):
        """ tictactoe specific move handling """
        # NOTE: temporary because we do not know yet what the move argument looks like
        self.lastMove.x = move.x
        self.lastMove.y = move.y
        super().handle_move(move)
