from game import STATUS_WINNER, STATUS_DRAW, TicTacToeGame
from players import BoardPlayerMixin, NamedPlayerMixin
from utils import Best


class AIPlayer(NamedPlayerMixin, BoardPlayerMixin):
    opponent = None

    def __init__(self, game: TicTacToeGame, *args, **kwargs):
        """ Initializes the AIPlayer instance """
        super().__init__(*args, **kwargs)
        self.game = game

    def play(self):
        """ Picks the best move, updates the board and prints the move to the the console """
        super().play()
        self.setup()
        self.do_move()
        print("AI placed {} on coords {},{}\n\n".format(self.name, self.board.last_turn[0], self.board.last_turn[1]))

    def setup(self):
        """ Sets up any initial properties """
        if self.opponent is None:
            for player in self.game.players:
                if player != self:
                    self.opponent = player
                    break

    def do_move(self):
        """ Attempts to calculate the best move and update the board accordingly """
        if self.board.last_turn is None:
            return self.board.set(1, 1, self)

        best_move = self.calc_best_move(self)
        self.board.set(best_move.row, best_move.column, self)

    def calc_best_move(self, player):
        """ Find best move for winning the game """
        # Don't go further if the game is in a WIN or DRAW state
        status, winner = self.game.state
        if status == STATUS_WINNER:
            return Best(3 if winner == self else 0)
        elif status == STATUS_DRAW:
            return Best(1)

        # Select opponent
        best_x, best_y = (0, 0)
        opp, v = (self.opponent, 0) if player == self else (self, 3)

        # Look for best move
        for x in range(3):
            for y in range(3):
                if self.board.is_available(x, y):
                    # Spot is free - do this move
                    self.board.set(x, y, player)
                    reply = self.calc_best_move(opp)
                    self.board.set(x, y, None)

                    # Check if current player is winning
                    if (player == self and reply.val > v) or (player == self.opponent and reply.val < v):
                        v, best_x, best_y = (reply.val, x, y)

        return Best(v, best_x, best_y)
