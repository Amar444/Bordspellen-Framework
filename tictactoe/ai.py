from players import BoardPlayerMixin, NamedPlayerMixin
from utils import Best


class AIPlayer(BoardPlayerMixin, NamedPlayerMixin):

    def __init__(self, game, *args, **kwargs):
        """ Initializes a new game and sets up the board class """
        super().__init__(*args, **kwargs)
        self.game = game

    def play(self):
        super().play()

    def choose_move(self, side=0):
        """ Find best move for winning the game """
        best_row = 0
        best_column = 0

        simple_eval = self.game.position_value()
        if simple_eval != self.board.UNCLEAR:
            return Best(simple_eval)

        # select opponent and value
        if side == self.board.COMPUTER:
            opp = self.board.HUMAN
            value = self.board.HUMAN_WIN
        else:
            opp = self.board.COMPUTER
            value = self.board.COMPUTER_WIN

        # look for best move
        for j in range(3):
            for i in range(3):
                if self.board.is_available(i, j):
                    # move to this square
                    self.board.set(i, j, side)
                    # continue playing
                    reply = self.choose_move(opp)
                    # clear position just used
                    self.board.set(i, j, None)

                    # check if current player is winning
                    if side == self.board.COMPUTER and reply.val > value or side == self.board.HUMAN and reply.val < value:
                        # current player is winning
                        value = reply.val
                        # coordinates best move
                        best_row = i
                        best_column = j
        return Best(value, best_row, best_column)
