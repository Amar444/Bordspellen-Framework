from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame


class TicTacToeBoard(TwoDimensionalBoard):
    """ Represents TicTacToe board """

    _ai_win = 3
    _opp_win = 0
    _draw = 1
    _unclear = 2

    @property
    def ai_win(self):
        return type(self)._ai_win

    @property
    def opp_win(self):
        return type(self)._opp_win

    @property
    def draw(self):
        return type(self)._draw

    @property
    def unclear(self):
        return type(self)._unclear

    size = 3, 3


class TicTacToeGame(TurnBasedGame, BoardGame):
    """ Represents TicTacToe game """
    board_class = TicTacToeBoard

    def position_value(self):
        """ Compute static value of current position (win, draw, etc.) """
        if self.is_a_win(self.players[1].name):
            return self.board.ai_win
        elif self.is_a_win(self.players[0].name):
            return self.board.opp_win
        elif self.board.is_full():
            return self.board.draw
        else:
            return self.board.unclear

    def is_a_win(self, side):
        """ Returns whether 'side' has won in this position """
        return self.is_a_win_horizontal(side) or self.is_a_win_vertical(side) or self.is_a_win_diagonal(side)

    def is_a_win_diagonal(self, side):
        """ Check diagonal win """
        # left top corner to right bottom corner
        if self.board.get(0, 0) == side and self.board.get(1, 1) == side and \
                self.board.get(2, 2) == side:
            return True
        # right top corner to left bottom corner
        if self.board.get(0, 2) == side and self.board.get(1, 1) == side and \
                self.board.get(2, 0) == side:
            return True
        return False

    def is_a_win_vertical(self, side):
        """ Check vertical win """
        is_a_win_vertical = False
        for col in range(3):
            if is_a_win_vertical is True:
                break
            temp = True
            for row in range(3):
                if self.board.get(row, col) != side:
                    temp = False
                is_a_win_vertical = temp
        return is_a_win_vertical

    def is_a_win_horizontal(self, side):
        """ Check horizontal win """
        is_a_win_horizontal = False
        for row in range(3):
            if is_a_win_horizontal is True:
                break
            temp = True
            for col in range(3):
                if self.board.get(row, col) != side:
                    temp = False
                is_a_win_horizontal = temp
        return is_a_win_horizontal

    def game_over(self):
        return self.position_value() != self.board.unclear

    def winner(self):
        if self.position_value() == self.board.ai_win:
            return "computer"
        elif self.position_value() == self.board.opp_win:
            return "human"
        else:
            return "nobody"
