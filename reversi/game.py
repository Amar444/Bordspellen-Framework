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

    @property
    def status(self):
        player_one, player_two = self.players
        if self.has_legal_moves(player_one) or self.has_legal_moves(player_two):
            return _UNCLEAR

        player_one_score, player_two_score = self.scores
        if player_one_score == player_two_score:
            return _DRAW
        elif player_one_score > player_two_score:
            return _PLAYER_ONE_WIN
        else:
            return _PLAYER_TWO_WIN

    @property
    def scores(self):
        # This calcs the scores for both players so that we don't have to loop over the
        # board state array twice - that's pretty expensive and this just saves us a
        # few clock cycles :)

        score_one = 0
        score_two = 0

        player_one = self.players[0]
        player_two = self.players[1]

        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                player = self.board.get(row, col)
                if player == player_one:
                    score_one += 1
                elif player == player_two:
                    score_two += 1

        return score_one, score_two

    def set_players(self, players: tuple):
        if len(players) != 2:
            raise Exception("You must play reversi with exactly two players.")

        super().set_players(players)

        self.board.set(3, 3, players[0])
        self.board.set(4, 4, players[0])
        self.board.set(3, 4, players[1])
        self.board.set(4, 3, players[1])

    def is_legal_move(self, player: Player, row: int, col: int):
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

    def iterate_legal_moves(self, player: Player):
        """ Iterates on all moves for the given player and yields all legal moves """
        rows, cols = self.board.size
        for row in range(rows):
            for col in range(cols):
                if len(self.is_legal_move(player, col, row)) > 0:
                    yield (row, col)

    def get_legal_moves(self, player: Player):
        """ Returns a list of legal moves for the given player """
        # You'd really want to use iterate_legal_moves due to memory consumption and other performance issues, tho
        return [move for move in self.iterate_legal_moves(player)]

    def has_legal_moves(self, player: Player):
        """ Checks wheter the given player has any legal moves left """
        for move in self.iterate_legal_moves(player):
            return True

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
