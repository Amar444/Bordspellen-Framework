""" This class provides the setup for an ReversiGame"""
""" HEAD
from reversi.game import ReversiGame
from reversi.ai import AIPlayer
from gac.players import BoardPlayerMixin, NamedPlayerMixin, Player
"""

from game import ReversiGame
from ai import ReversiAIPlayer
from players import BoardPlayerMixin, NamedPlayerMixin, Player


class DemoCliPlayer(NamedPlayerMixin, BoardPlayerMixin):
    opponent = None

    def play(self):
        super().play()
        if len(self.game.get_legal_moves(self)) == 0:
            return
        try:
            x, y = str(input("Please enter coords to update the board? [x,y] ")).split(',')
            game.execute_move(self, int(x), int(y))
            print("\n")
        except Exception as e:
            print("{}\n".format(e))
            self.setup()
            self.play()

    def setup(self):
        """ Sets up any initial properties """
        if self.opponent is None:
            for player in self.game.players:
                if player != self:
                    self.opponent = player
                    break


game = ReversiGame()
players = []

answer = str(input("Choose a gametype:\n"
                   "1: Human vs Human\n"
                   "2: Human vs AI\n"
                   "3: AI vs AI\n"))
if answer == "3":
    players += (ReversiAIPlayer(name="W", game=game), ReversiAIPlayer(name="B", game=game),)
elif answer == "2":
    players += (DemoCliPlayer(name="W", game=game), ReversiAIPlayer(name="B", game=game), )
else:
    players += (DemoCliPlayer(name="W", game=game), DemoCliPlayer(name="B", game=game), )
game.set_players(players)
game.play()
