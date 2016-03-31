"""
Provides implementation for Player objects
"""

from utils import Best


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


class TicTacToeAI(Player):
    """ Player mixin that supports TicTacToe AI """

    OPP_WIN = 0
    DRAW = 1
    UNCLEAR = 2
    AI_WIN = 3

    def __init__(self, ai: int, opp: int, *args, **kwargs):
        self.ai = ai
        self.opp = opp
        super().__init__(*args, **kwargs)

    def play(self):
        self.choose_move(self.ai)

    def choose_move(self, side):
        """ Find best move for winning the game """
        best_row = 0
        best_column = 0

        simple_eval = self.position_value()
        if simple_eval != self.UNCLEAR:
            return Best(simple_eval)

        # select opponent and value
        if side == self.ai:
            opp, value = (self.opp, self.OPP_WIN)
        else:
            opp, value = (self.ai, self.AI_WIN)

        # look for best move
        for j in range(self.COLUMN_COUNT):
            for i in range(self.ROW_COUNT):
                if self.square_is_empty(i, j):
                    # move to this square
                    self.place(i, j, side)
                    # continue playing
                    reply = self.choose_move(opp)
                    # clear position just used
                    self.place(i, j, self.EMPTY)

                    # check if current player is winning
                    if side == self.ai and reply.val > value or side == self.opp and reply.val < value:
                        # current player is winning
                        value = reply.val
                        # coordinates best move
                        best_row = i
                        best_column = j
        return Best(value, best_row, best_column)

    def position_value(self):
        """ Compute static value of current position (win, draw, etc.) """
        if self.is_a_win(self.ai):
            return self.AI_WIN
        elif self.is_a_win(self.opp):
            return self.OPP_WIN
        elif self.board_is_full():
            return self.DRAW
        else:
            return self.UNCLEAR
