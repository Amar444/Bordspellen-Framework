from game import STATUS_WINNER, STATUS_DRAW
from players import BoardPlayerMixin, NamedPlayerMixin


class AIPlayer(NamedPlayerMixin, BoardPlayerMixin):
    opponent = None

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
            return self.board.set(1, 1, self, False)

        i, row, column = best_move = self.calc_best_move(self)
        self.board.set(row, column, self, False)

    def calc_best_move(self, player):
        """ Find best move for winning the game """
        # Don't go further if the game is in a WIN or DRAW state
        status, winner = self.game.state

        if status == STATUS_WINNER:
            return 3 if winner == self else 0, 0, 0
        elif status == STATUS_DRAW:
            return 1, 0, 0

        # Select opponent
        best_x, best_y = (0, 0)
        opp, v = (self.opponent, 0) if player == self else (self, 3)
        board = self.board.state

        # Look for best move
        for y in range(3):
            for x in range(3):
                if board[x][y] is None:
                    # Spot is free - do this move
                    board[x][y] = player
                    val, _, _ = self.calc_best_move(opp)
                    board[x][y] = None

                    # Check if current player is winning
                    if (player == self and val > v) or (player == self.opponent and val < v):
                        v, best_x, best_y = (val, x, y)

        return v, best_x, best_y
