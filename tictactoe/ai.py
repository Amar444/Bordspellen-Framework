from players import BoardPlayerMixin, NamedPlayerMixin, CommandLineInputPlayerMixin
from utils import Best


class AIPlayer(BoardPlayerMixin, NamedPlayerMixin):

    def __init__(self, game, *args, **kwargs):
        """ Initializes a new game and sets up the board class """
        super().__init__(*args, **kwargs)
        self.game = game

    def play(self):
        best_move = self.choose_move(self.name)
        self.board.set(best_move.row, best_move.column, self.name)

    def choose_move(self, side=0):
        """ Find best move for winning the game """
        best_row = 0
        best_column = 0

        simple_eval = self.game.position_value()
        if simple_eval != self.board.unclear:
            return Best(simple_eval)

        # select opponent and value
        if side == self.name:
            opp, value = (self.game.players[0], self.board.opp_win)
        else:
            opp, value = (self.game.players[1], self.board.ai_win)

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
                    if side == self.name and reply.val > value or side == self.game.players[0] and reply.val < value:
                        # current player is winning
                        value = reply.val
                        # coordinates best move
                        best_row = i
                        best_column = j
        return Best(value, best_row, best_column)


class DemoTicTacToePlayer(BoardPlayerMixin, NamedPlayerMixin, CommandLineInputPlayerMixin):
    def play(self):
        super().play()
