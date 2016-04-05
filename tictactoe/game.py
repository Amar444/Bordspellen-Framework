from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame

STATUS_UNCLEAR = 0
STATUS_WINNER = 1
STATUS_DRAW = 2


class TicTacToeBoard(TwoDimensionalBoard):
    """ Represents a TicTacToe board """
    size = (3, 3)


class TicTacToeGame(TurnBasedGame, BoardGame):
    """ Represents TicTacToe game """
    board = TicTacToeBoard()

    @property
    def state(self):
        winner = self.winner
        if self.board.is_full():
            if winner is None:
                return STATUS_DRAW, None
            return STATUS_WINNER, winner
        else:
            if winner is None:
                return STATUS_UNCLEAR, None
            return STATUS_WINNER, winner

    @property
    def status(self):
        return self.state[0]

    @property
    def winner(self):
        if self.has_won(self.players[0]):
            return self.players[0]
        elif self.has_won(self.players[1]):
            return self.players[1]
        else:
            return None

    def has_won(self, player):
        """ Returns whether 'side' has won in this position """
        return self.has_won_horizontal(player) or self.has_won_vertical(player) or self.has_won_diagonal(player)

    def has_won_horizontal(self, player):
        """ Check horizontal win for the given player """
        winning = (player,)*3
        return (self.board.get(0, 0), self.board.get(0, 1), self.board.get(0, 2)) == winning or \
               (self.board.get(1, 0), self.board.get(1, 1), self.board.get(1, 2)) == winning or \
               (self.board.get(2, 0), self.board.get(2, 1), self.board.get(2, 2)) == winning

    def has_won_vertical(self, player):
        """ Check vertical win for the given player """
        winning = (player,)*3
        return (self.board.get(0, 0), self.board.get(1, 0), self.board.get(2, 0)) == winning or \
               (self.board.get(0, 1), self.board.get(1, 1), self.board.get(2, 1)) == winning or \
               (self.board.get(0, 2), self.board.get(1, 2), self.board.get(2, 2)) == winning

    def has_won_diagonal(self, player):
        """ Check diagonal win for the given player """
        winning = (player,)*3
        return (self.board.get(0, 0), self.board.get(1, 1), self.board.get(2, 2)) == winning or \
               (self.board.get(0, 2), self.board.get(1, 1), self.board.get(2, 0)) == winning

    def next_turn(self):
        """ Check, for each turn, whether someone has won already """
        super().next_turn()
        status = self.status
        if status != STATUS_UNCLEAR:
            print(self.board)
            if status == STATUS_WINNER:
                self.is_playing = False
                print("Game over! Player {} has won this round!".format(self.winner))
            elif status == STATUS_DRAW:
                self.is_playing = False
                print("Game over! It's a tie!")
