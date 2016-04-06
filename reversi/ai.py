""" Provides artificial intelligence for the Reversi game"""
from game import ReversiGame, _UNCLEAR, _PLAYER_ONE_WIN, _PLAYER_TWO_WIN, _DRAW
from players import BoardPlayerMixin, NamedPlayerMixin
from utils import Best
import copy

class AIPlayer(NamedPlayerMixin, BoardPlayerMixin):
    opponent = None
    board_value_method = "greedy"

    def __init__(self, game: ReversiGame, *args, **kwargs):
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
        best_move = self.calc_best_move(self)
        self.game.execute_move(self, best_move.row, best_move.col)

    def calc_best_move(self, player, depth: int):
        """ Find best move for winning the game """
        if depth == 0:
            # return board value if max depth is reached
            return self.calc_value(player, self.board_value_method)
        if self.board.get_value() == _UNCLEAR:
            best_reply = Best(99,0,0) if player == self.opponent else Best(0,0,0)
            # iterate over all possible moves
            moves = self.game.get_legal_moves(player)
            board_state = copy.deepcopy(self.board.state)
            if len(moves) == 0:
                # skip if no possible moves
                return self.calc_best_move(self if player == self.opponent else self.opponent, depth-1)
            for move in self.game.get_legal_moves(player):
                self.game.execute_move(player, move[0], move[1])
                reply = self.calc_best_move(self if player == self.opponent else self.opponent, depth-1)
                self.board.state = board_state
                # set as best reply if lowest or highest value
                if (player == self and reply.val > best_reply.val) or \
                        (player == self.opponent and reply.val < best_reply.val):
                    best_reply = reply
            return best_reply

        else:
            # return game value if game has ended, when losing try to lose the least :P
            return Best(self.calc_value(player, self.board_value_method))

    def calc_value(self, player, method: str):
        # greedy board value for minimax, You want max stones, opponent wants you to have min stones
        if method == "greedy":
            return self.game.get_score(self)
