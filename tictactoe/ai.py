from game import STATUS_WINNER, STATUS_DRAW
from players import BoardPlayerMixin, NamedPlayerMixin
from utils import Best


class AIPlayer(BoardPlayerMixin, NamedPlayerMixin):
    opponent = None

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game = game

    def play(self):
        if self.opponent is None:
            for player in self.game.players:
                if player != self:
                    self.opponent = player
                    break

        if self.board.last_turn is None:
            return self.board.set(1, 1, self)

        best_move = self.choose_move(self)
        self.board.set(best_move.row, best_move.column, self)

    def choose_move(self, player):
        """ Find best move for winning the game """
        best_row = 0
        best_column = 0

        status, winner = self.game.state
        if status == STATUS_WINNER:
            return Best(3 if winner == self else 0)
        elif status == STATUS_DRAW:
            return Best(1)

        # select opponent and value
        if player == self:
            opp, value = (self.opponent, 0)
        else:
            opp, value = (self, 3)

        # look for best move
        for col in range(3):
            for row in range(3):
                if self.board.is_available(row, col):
                    # move to this square
                    self.board.set(row, col, player)
                    # continue playing
                    reply = self.choose_move(opp)
                    # clear position just used
                    self.board.set(row, col, None)

                    # check if current player is winning
                    if (player == self and reply.val > value) or \
                            (player == self.opponent and reply.val < value):
                        # current player is winning
                        value = reply.val
                        # coordinates best move
                        best_row = row
                        best_column = col
        return Best(value, best_row, best_column)
