""" Provides tools to enforce game rules and keep track of the game """

from gac.boards import TwoDimensionalBoard
from gac.games import BoardGame, TurnBasedGame

REVERSI_BOARD_SIZE = 8

#Represtents the 8 directions, N, S, E, W, NW, NE, SW, SE in no particular order
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1 ,-1), (1, 0), (1,1)]

class ReversiBoard(TwoDimensionalBoard):
    """ Represents an reversi board"""

    size = (REVERSI_BOARD_SIZE, REVERSI_BOARD_SIZE)

class ReversiGame(TurnBasedGame, BoardGame):
    """ Represents Reversi game"""
    board_class = ReversiBoard


    def is_legal_move(self, player: any, row: int, col: int):
        """Determine if the play on a square is an legal move"""
        if self.board.isAvaiable() is False:
            return False
        for direction in range(len(DIRECTIONS)):
            spotted_opponent = False
            for distance in range(REVERSI_BOARD_SIZE):
                row_to_check = row + distance * DIRECTIONS[direction][0]
                col_to_check = col + distance * DIRECTIONS[direction][1]
                try:
                    self.board.checkCoordinates(row_to_check, col_to_check)
                    stone = self.board.get(row_to_check, col_to_check)
                    if stone == player:
                        break
                    elif stone is None and spotted_opponent == False:
                        break
                    elif stone is None and spotted_opponent:
                        return True
                    else:
                        spotted_opponent = True
                except:
                    break
        return False



    def get_legal_moves(self, player: any):
        """ Functions that figures out whic legal moves there currently are for the player"""
        moves = []
        for row in range(REVERSI_BOARD_SIZE):
            for col in range(REVERSI_BOARD_SIZE):
                if self.is_legal_move():
                    moves.append((row,col))
        return moves
