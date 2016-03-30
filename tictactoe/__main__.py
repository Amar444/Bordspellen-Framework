from random import randint


class TicTacToe(object):
    """
    Represents TicTacToe game.
    """

    ROW_COUNT = 3
    COLUMN_COUNT = 3
    HUMAN = 2
    COMPUTER = 1
    EMPTY = 0
    HUMAN_WIN = 0
    DRAW = 1
    UNCLEAR = 2
    COMPUTER_WIN = 3

    position = UNCLEAR

    def __init__(self):
        """ Constructor """
        self.side = randint(1, 2)
        self.Matrix = [[0 for x in range(self.ROW_COUNT)] for x in range(self.COLUMN_COUNT)]
        self.clear_board()

    def set_computer_plays(self):
        self.side = self.COMPUTER

    def set_human_plays(self):
        self.side = self.HUMAN

    def computer_plays(self):
        return self.side == self.COMPUTER

    def choose_move2(self):
        best = self.choose_move(self.COMPUTER)
        return best.row * 3 + best.column

    def choose_move(self, side=0):
        """ Find best move for winning the game """
        best_row = 0
        best_column = 0

        simple_eval = self.position_value()
        if simple_eval != self.UNCLEAR:
            return self.Best(simple_eval)

        # select opponent and value
        if side == self.COMPUTER:
            opp = self.HUMAN
            value = self.HUMAN_WIN
        else:
            opp = self.COMPUTER
            value = self.COMPUTER_WIN

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
                    if side == self.COMPUTER and reply.val > value or side == self.HUMAN and reply.val < value:
                        # current player is winning
                        value = reply.val
                        # coordinates best move
                        best_row = i
                        best_column = j
        return self.Best(value, best_row, best_column)

    def move_ok(self, move):
        """ Check if move is ok """
        return 0 <= move <= 8 and self.Matrix[int(move/3)][int(move % 3)] == self.EMPTY

    def play_move(self, move):
        """ Play the move """
        self.Matrix[int(move/3)][int(move % 3)] = self.side
        if self.side == self.COMPUTER:
            self.side = self.HUMAN
        else:
            self.side = self.COMPUTER

    def clear_board(self):
        """ Clears board """
        self.Matrix = [[0 for x in range(self.ROW_COUNT)] for x in range(self.COLUMN_COUNT)]

    def get_board(self):
        return self.Matrix

    def board_is_full(self):
        """ Check whether the board is full. The method is doing this with checking the entries in the two arrays from
            the board and will directly return it's result when it finds out if there is still place for another move"""
        for j in range(self.COLUMN_COUNT):
            for i in range(self.ROW_COUNT):
                # '0' means there is still space
                if self.Matrix[i][j] == 0:
                    return False
        return True

    def is_a_win(self, side):
        """ Returns whether 'side' has won in this position """
        return self.is_a_win_horizontal(side) or self.is_a_win_vertical(side) or self.is_a_win_diagonal(side)

    def is_a_win_diagonal(self, side):
        """ Check diagonal win """
        # left top corner to right bottom corner
        if self.Matrix[0][0] == side and self.Matrix[1][1] == side and self.Matrix[2][2] == side:
            return True
        # right top corner to left bottom corner
        if self.Matrix[0][2] == side and self.Matrix[1][1] == side and self.Matrix[2][0] == side:
            return True
        return False

    def is_a_win_vertical(self, side):
        """ Check vertical win """
        is_a_win_vertical = False
        for i in range(self.COLUMN_COUNT):
            if is_a_win_vertical is True:
                break
            temp = True
            for j in range(self.ROW_COUNT):
                if self.Matrix[j][i] != side:
                    temp = False
                is_a_win_vertical = temp
        return is_a_win_vertical

    def is_a_win_horizontal(self, side):
        """ Check horizontal win """
        is_a_win_horizontal = False
        for i in range(self.ROW_COUNT):
            if is_a_win_horizontal is True:
                break
            temp = True
            for j in range(self.COLUMN_COUNT):
                if self.Matrix[i][j] != side:
                    temp = False
                is_a_win_horizontal = temp
        return is_a_win_horizontal

    def place(self, row, column, piece):
        """ Play a move, possibly clearing a square """
        self.Matrix[row][column] = piece

    def square_is_empty(self, row, column):
        return self.Matrix[row][column] == self.EMPTY

    def position_value(self):
        """ Compute static value of current position (win, draw, etc.) """
        if self.is_a_win(self.COMPUTER):
            return self.COMPUTER_WIN
        elif self.is_a_win(self.HUMAN):
            return self.HUMAN_WIN
        elif self.board_is_full():
            return self.DRAW
        else:
            return self.UNCLEAR

    def game_over(self):
        self.position = self.position_value()
        return self.position != self.UNCLEAR

    def winner(self):
        if self.position == self.COMPUTER_WIN:
            return "computer"
        elif self.position == self.HUMAN_WIN:
            return "human"
        else:
            return "nobody"

    class Best(object):
        def __init__(self, v, r=0, c=0):
            self.val = v
            self.row = r
            self.column = c
