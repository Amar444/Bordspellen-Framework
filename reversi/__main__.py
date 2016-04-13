""" This class provides the setup for an ReversiGame"""

from reversi.game import ReversiGame
from reversi.ai import AIPlayer
from gac.players import BoardPlayerMixin, NamedPlayerMixin, Player


class DemoCliPlayer(NamedPlayerMixin, BoardPlayerMixin):
    def play(self):
        super().play()
        if len(self.game.get_legal_moves == 0):
            return
        try:
            x, y = str(input("Please enter coords to update the board? [x,y] ")).split(',')
            game.execute_move(self, int(x), int(y))
            print("\n")
        except Exception as e:
            print("{}\n".format(e))
            self.play()


game = ReversiGame()
players = []

answer = str(input("Choose a gametype:\n"
                   "1: Human vs Human\n"
                   "2: Human vs AI\n"
                   "3: AI vs AI\n"))
if answer == "3":
    players += (AIPlayer(name="W", board=game.board, game=game), AIPlayer(name="B", board=game.board, game=game),)
elif answer == "2":
    players += (DemoCliPlayer(name="W", board=game.board), AIPlayer(name="B", board=game.board), )
else:
    players += (DemoCliPlayer(name="W", board=game.board), DemoCliPlayer(name="B", board=game.board), )
game.set_players(players)
game.play()
