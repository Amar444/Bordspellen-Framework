from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame

STATUS_UNCLEAR = 0
STATUS_WINNER = 1
STATUS_DRAW = 2


class TicTacToeBoard(TwoDimensionalBoard):
    """ Represents a TicTacToe board """
    size = (3, 3)

    @property
    def winner(self):
        return self.winner_horizontal or self.winner_vertical or self.winner_diagonal

    @property
    def winner_horizontal(self):
        """ Check horizontal win for the given player """
        state = self.state
        if state[0][0] == state[0][1] == state[0][2]:
            return state[0][0]
        elif state[1][0] == state[1][1] == state[1][2]:
            return state[1][0]
        elif state[2][0] == state[2][1] == state[2][2]:
            return state[2][0]
        return None

    @property
    def winner_vertical(self):
        """ Check vertical win for the given player """
        state = self.state
        if state[0][0] == state[1][0] == state[2][0]:
            return state[0][0]
        elif state[0][1] == state[1][1] == state[2][1]:
            return state[0][1]
        elif state[0][2] == state[1][2] == state[2][2]:
            return state[0][2]
        return None

    @property
    def winner_diagonal(self):
        """ Check diagonal win for the given player """
        state = self.state
        if state[0][0] == state[1][1] == state[2][2]:
            return state[0][0]
        elif state[0][2] == state[1][1] == state[2][0]:
            return state[0][2]
        return None


class TicTacToeGame(TurnBasedGame, BoardGame):
    """ Represents TicTacToe game """
    name = "Tic-tac-toe"
    board_class = TicTacToeBoard

    @property
    def state(self):
        winner = self.board.winner
        if winner:
            return STATUS_WINNER, winner

        return STATUS_DRAW if self.board.is_full() else STATUS_UNCLEAR, None

    @property
    def status(self):
        return self.state[0]

    def next_turn(self):
        """ Check, for each turn, whether someone has won already """
        super().next_turn()
        status = self.status
        if status != STATUS_UNCLEAR:
            print(self.board)
            if status == STATUS_WINNER:
                self.is_playing = False
                print("Game over! Player {} has won this round!".format(self.board.winner))
            elif status == STATUS_DRAW:
                self.is_playing = False
                print("Game over! It's a tie!")
