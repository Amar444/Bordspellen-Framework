""" Provides tools to enforce game rules and keep track of the game """

from boards import TwoDimensionalBoard
from games import BoardGame, TurnBasedGame
from exceptions import InvalidCoordinatesException
from players import Player

_REVERSI_BOARD_SIZE = 8

# Represents the 8 directions, N, S, E, W, NW, NE, SW, SE in no particular order
_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Game values
_PLAYER_ONE_WIN = 3
_UNCLEAR = 2
_DRAW = 1
_PLAYER_TWO_WIN = 0


class ReversiBoard(TwoDimensionalBoard):
    """ Represents an reversi board"""
    size = (_REVERSI_BOARD_SIZE, _REVERSI_BOARD_SIZE)


class ReversiGame(TurnBasedGame, BoardGame):
    """ Represents Reversi game"""
    board_class = ReversiBoard

    def init_board(self, player_one: Player, player_two: Player):
        self.board.set(3, 3, player_one.name[0:1])
        self.board.set(4, 4, player_one.name[0:1])
        self.board.set(3, 4, player_two.name[0:1])
        self.board.set(4, 3, player_two.name[0:1])

    def is_legal_move(self, player: any, row: int, col: int):
        """Determine if the play on a square is an legal move"""
        if self.board.is_available(row, col) is False:
            return []
        capture_directions = []
        for direction in range(len(_DIRECTIONS)):
            spotted_opponent = False
            for distance in range(max(self.board.size)):
                row_to_check = row + (distance + 1) * _DIRECTIONS[direction][0]
                col_to_check = col + (distance + 1) * _DIRECTIONS[direction][1]
                try:
                    self.board.check_coordinates(row_to_check, col_to_check)
                    stone = self.board.get(row_to_check, col_to_check)
                    if stone is None:
                        break
                    elif stone == player and not spotted_opponent:
                        break
                    elif stone == player and spotted_opponent:
                        capture_directions.append(direction)
                        break
                    else:
                        spotted_opponent = True
                except InvalidCoordinatesException:
                    break
        return capture_directions

    def get_legal_moves(self, player: any):
        """ Functions that figures out which legal moves there currently are for the player"""
        moves = []
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                if len(self.is_legal_move(player, row, col)) > 0:
                    moves.append((row, col))
        return moves

    def execute_move(self, player, row, col):
        """ Places a stone on the board and flips the opponents stones"""
        directions = self.is_legal_move(player, row, col)
        if len(directions) == 0:
            raise ValueError("{} is not allowed to play at {},{} at this time.".format(player, row, col))
        self.board.set(row, col, player)
        for direction in directions:
            for distance in range(max(self.board.size)):
                col_to_change = col + (distance + 1) * _DIRECTIONS[direction][1]
                row_to_change = row + (distance + 1) * _DIRECTIONS[direction][0]
                if self.board.get(row_to_change, col_to_change) == player:
                    break
                elif self.board.get(row_to_change, col_to_change) is None:
                    print("How the hell did you get here?")
                else:
                    self.board.set(row_to_change, col_to_change, player)

    def get_score(self, player: any):
        score = 0
        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                if self.board.get(row, col) == player:
                    score += 1
        return score

    def get_value(self, player_one: any, player_two: any):
        player_one_has_moves = len(self.get_legal_moves(player_one)) > 0
        player_two_has_moves = len(self.get_legal_moves(player_two)) > 0
        if player_one_has_moves or player_two_has_moves:
            return _UNCLEAR
        player_one_score = self.get_score(player_one)
        player_two_score = self.get_score(player_two)
        if player_one_score == player_two_score:
            return _DRAW
        if player_one_score > player_two_score:
            return _PLAYER_ONE_WIN
        else:
            return _PLAYER_TWO_WIN
