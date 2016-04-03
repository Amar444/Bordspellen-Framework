""" Provides tools to enforce game rules and keep track of the game """

from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame

REVERSI_BOARD_SIZE = 8

# Represtents the 8 directions, N, S, E, W, NW, NE, SW, SE in no particular order
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class ReversiBoard(TwoDimensionalBoard):
    """ Represents an reversi board"""

    size = (REVERSI_BOARD_SIZE, REVERSI_BOARD_SIZE)


class ReversiGame(TurnBasedGame, BoardGame):
    """ Represents Reversi game"""
    board_class = ReversiBoard

    def is_legal_move(self, player: any, row: int, col: int):
        """Determine if the play on a square is an legal move"""
        if self.board.is_available(row, col) is False:
            return []
        capture_directions = []
        for direction in range(len(DIRECTIONS)):
            spotted_opponent = False
            for distance in range(REVERSI_BOARD_SIZE):
                row_to_check = row + (distance+1) * DIRECTIONS[direction][0]
                col_to_check = col + (distance+1) * DIRECTIONS[direction][1]
                try:
                    self.board.check_coordinates(row_to_check, col_to_check)
                    stone = self.board.get(row_to_check, col_to_check)
                    if stone is None:
                        break
                    elif stone == player and spotted_opponent == False:
                        break
                    elif stone == player and spotted_opponent:
                        capture_directions.append(direction)
                        break
                    else:
                        spotted_opponent = True
                except Exception as e:
                    # print(e)
                    break
        return capture_directions

    def get_legal_moves(self, player: any):
        """ Functions that figures out whic legal moves there currently are for the player"""
        moves = []
        for row in range(REVERSI_BOARD_SIZE):
            for col in range(REVERSI_BOARD_SIZE):
                if len(self.is_legal_move(player, row, col)) > 0:
                    moves.append((row, col))
        return moves