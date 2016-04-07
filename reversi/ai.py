""" Provides artificial intelligence for the Reversi game"""
from game import ReversiGame, _UNCLEAR, _PLAYER_ONE_WIN, _PLAYER_TWO_WIN, _DRAW
from players import BoardPlayerMixin, NamedPlayerMixin
from utils import Best



class AIPlayer(NamedPlayerMixin, BoardPlayerMixin):
    opponent = None
    board_value_method = "greedy"
    _DEFAULT_DEPTH = 2

    def __init__(self, game: ReversiGame, depth=_DEFAULT_DEPTH, *args, **kwargs):
        """ Initializes the AIPlayer instance """
        super().__init__(*args, **kwargs)
        self.game = game
        self.depth = depth

    def play(self):
        """ Picks the best move, updates the board and prints the move to the the console """
        super().play()
        if len(self.game.get_legal_moves(self)) == 0:
            return
        self.setup()
        self.do_move()

    def setup(self):
        """ Sets up any initial properties """
        if self.opponent is None:
            for player in self.game.players:
                if player != self:
                    self.opponent = player
                    break

    def do_move(self):
        """ Attempts to calculate the best move and update the board accordingly """
        print(self.game.get_legal_moves(self))
        best_move = self.calc_best_move(self, self.depth)
        print(self.game.board.__str__())
        print(self.game.get_legal_moves(self))
        self.game.execute_move(self, best_move.row, best_move.column)
        print("AI placed {} on coords {},{}\n\n".format(self.name, best_move.row, best_move.column))

    def calc_best_move(self, player, depth: int):
        """ Find best move for winning the game """
        if depth == 0:
            # return board value if max depth is reached
            return Best(self.calc_value(player, self.board_value_method))
        if self.game.status == _UNCLEAR:
            best_reply = None
            # iterate over all possible moves
            if not self.game.has_legal_moves(player):
                # skip if no possible moves
                return self.calc_best_move(self if player == self.opponent else self.opponent, depth-1)
            for move in self.game.iterate_legal_moves(player):
                board_state = [[] for x in range(len(self.board.state))]
                for row in range(len(board_state)):
                    for element in self.game.board.state[row]:
                        board_state[row].append(element)
                self.game.execute_move(player, move[0], move[1])
                reply = self.calc_best_move(self if player == self.opponent else self.opponent, depth-1)
                self.game.board.state = board_state
                # set as best reply if lowest or highest value
                if (best_reply is None or player == self and reply.val > best_reply.val) or \
                        (player == self.opponent and reply.val < best_reply.val):
                    best_reply = Best(reply.val, move[0], move[1])
            return best_reply

        else:
            # return game value if game has ended, when losing try to lose the least :P
            return Best(self.calc_value(player, self.board_value_method))

    def calc_value(self, player, method: str):
        # greedy board value for minimax, You want max stones, opponent wants you to have min stones
        if method == "greedy":
            return self.game.scores[0 if self == self.game.players[0] else 1]
