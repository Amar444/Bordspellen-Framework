""" Provides tools to enforce game rules and keep track of the game """
import time

from gac.boards import TwoDimensionalBoard
from gac.games import BoardGame, TurnBasedGame
from gac.exceptions import InvalidCoordinatesException
from gac.players import Player

_REVERSI_BOARD_SIZE = 8

# Represents the 8 directions, N, S, E, W, NW, NE, SW, SE in no particular order
_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Game values
_PLAYER_ONE_WIN = 3
_UNCLEAR = 2
_DRAW = 1
_PLAYER_TWO_WIN = 0
_SQUARE_WEIGHTS = [
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
    [0, 120, -20,  20,   5,   5,  20, -20, 120,   0],
    [0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0],
    [0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0],
    [0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0],
    [0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0],
    [0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0],
    [0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0],
    [0, 120, -20,  20,   5,   5,  20, -20, 120,   0],
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0]
]


class ReversiBoard(TwoDimensionalBoard):
    """ Represents an reversi board"""
    size = (_REVERSI_BOARD_SIZE, _REVERSI_BOARD_SIZE)


class ReversiGame(TurnBasedGame, BoardGame):
    """ Represents Reversi game"""
    board_class = ReversiBoard
    legal_move_cache = {}
    _max_board_size = None

    @property
    def max_board_size(self):
        if not self._max_board_size:
            self._max_board_size = max(self.board.size) + 1
        return self._max_board_size

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

        state = self.board.state

        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                player = state[row][col]
                if player == player_one:
                    score_one += 1
                elif player == player_two:
                    score_two += 1

        return score_one, score_two

    def weighted_scores(self, player):
        """
        Compute the difference between the sum of the weights of player's
        squares and the sum of the weights of opponent's squares.
        """
        opp = player.opponent
        total = 0
        state = self.board.state

        for row in range(self.board.size[0]):
            for col in range(self.board.size[1]):
                current_player = state[row][col]
                if current_player == player:
                    total += _SQUARE_WEIGHTS[row][col]
                elif current_player == opp:
                    total -= _SQUARE_WEIGHTS[row][col]
        return total

    def set_players(self, players: tuple):
        if len(players) != 2:
            raise Exception("You must play reversi with exactly two players.")

        super().set_players(players)

        self.board.set(3, 3, players[0])
        self.board.set(4, 4, players[0])
        self.board.set(3, 4, players[1])
        self.board.set(4, 3, players[1])

    def is_legal_move(self, player: Player, row: int, col: int, just_check: bool=False):
        """Determine if the play on a square is an legal move"""
        rows, cols = self.board.size

        if row < 0 or col < 0 or row >= rows or col >= cols or \
                not self.board.is_available(row, col, False):
            return False if just_check else []

        state = self.board.state
        capture_directions = []
        max_board_size = self.max_board_size

        for multiplier_row, multiplier_col in _DIRECTIONS:
            spotted_opponent = False
            for distance in range(1, max_board_size):
                row_to_check = row + distance * multiplier_row
                col_to_check = col + distance * multiplier_col

                if row_to_check < 0 or col_to_check < 0 or row_to_check >= rows or col_to_check >= cols:
                    break

                stone = state[row_to_check][col_to_check]
                if not stone:
                    break
                elif stone == player:
                    if spotted_opponent:
                        if just_check:
                            return True
                        capture_directions.append((multiplier_row, multiplier_col))
                    break
                else:
                    spotted_opponent = True

        return False if just_check else capture_directions

    def iterate_legal_moves(self, player: Player):
        """ Iterates on all moves for the given player and yields all legal moves """
        rows, cols = self.board.size
        for row in range(rows):
            for col in range(cols):
                if self.is_legal_move(player, row, col, True):
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
        state = self.board.state

        if len(directions) == 0:
            raise ValueError("{} is not allowed to play at {},{} at this time.".format(player, row, col))

        resets = [(row, col, state[row][col])]
        state[row][col] = player
        max_distance = range(1, self.max_board_size)

        for dir_row, dir_col in directions:
            for distance in max_distance:
                row_to_change = row + distance * dir_row
                col_to_change = col + distance * dir_col

                current = state[row_to_change][col_to_change]

                if current == player:
                    break
                elif current is not None:
                    resets.append((row_to_change, col_to_change, current))
                    state[row_to_change][col_to_change] = player

        return resets

    def next_turn(self):
        """ Check, for each turn, whether someone has won already """
        current_milli_time = lambda: int(round(time.time() * 1000))
        start = current_milli_time()
        status = self.status
        if status != _UNCLEAR:
            if status == _PLAYER_TWO_WIN or status == _PLAYER_ONE_WIN:
                self.is_playing = False
                scores = self.scores
                print("Game over! Player {} has won this round! with a score of {} to {}"
                      .format(self.players[0] if status == _PLAYER_ONE_WIN else
                              self.players[1], scores[0], scores[1]))
            elif self.status == _DRAW:
                self.is_playing = False
                print("Game over! It's a tie!")
        super().next_turn()
        end = current_milli_time()
        print("Turn took {} seconds".format(float(end-start)/1000.0))
