from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame


class TicTacToeBoard(TwoDimensionalBoard):
    size = 3, 3


class TicTacToeGame(TurnBasedGame, BoardGame):
    board_class = TicTacToeBoard
