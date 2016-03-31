from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame


class TicTacToeBoard(TwoDimensionalBoard):
    """ Represents TicTacToe board """

    AI_WIN = 3
    OPP_WIN = 0
    DRAW = 1
    UNCLEAR = 2

    size = 3, 3


class TicTacToeGame(TurnBasedGame, BoardGame):
    """ Represents TicTacToe game """
    board_class = TicTacToeBoard

    def position_value(self):
        """ Compute static value of current position (win, draw, etc.) """
        if self.is_a_win(self.players(1)):
            return self.board.AI_WIN
        elif self.is_a_win(self.players(0)):
            return self.board.OPP_WIN
        elif self.board.is_full(self.board):
            return self.board.DRAW
        else:
            return self.board.UNCLEAR

    def is_a_win(self, side):
        """ Returns whether 'side' has won in this position """
        return self.is_a_win_horizontal(side) or self.is_a_win_vertical(side) or self.is_a_win_diagonal(side)

    def is_a_win_diagonal(self, side):
        """ Check diagonal win """
        # left top corner to right bottom corner
        if self.board.get(self.board, 0, 0) == side and self.board.get(self.board, 1, 1) == side and \
                self.board.get(self.board, 2, 2) == side:
            return True
        # right top corner to left bottom corner
        if self.board.get(self.board, 0, 2) == side and self.board.get(self.board, 1, 1) == side and \
                self.board.get(self.board, 2, 0) == side:
            return True
        return False

    def is_a_win_vertical(self, side):
        """ Check vertical win """
        is_a_win_vertical = False
        for i in range(3):
            if is_a_win_vertical is True:
                break
            temp = True
            for j in range(3):
                if self.board.get(self.board, j, i) != side:
                    temp = False
                is_a_win_vertical = temp
        return is_a_win_vertical

    def is_a_win_horizontal(self, side):
        """ Check horizontal win """
        is_a_win_horizontal = False
        for i in range(3):
            if is_a_win_horizontal is True:
                break
            temp = True
            for j in range(3):
                if self.board.get(self.board, i, j) != side:
                    temp = False
                is_a_win_horizontal = temp
        return is_a_win_horizontal

    def game_over(self):
        return self.position_value() != self.board.UNCLEAR

    def winner(self):
        if self.position_value() == self.board.AI_WIN:
            return "computer"
        elif self.position_value() == self.board.OPP_WIN:
            return "human"
        else:
            return "nobody"
