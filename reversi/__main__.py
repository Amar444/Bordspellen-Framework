""" This class provides the setup for an ReversiGame"""

from game import ReversiGame
from ai import AIPlayer
from players import BoardPlayerMixin, NamedPlayerMixin, Player


class DemoCliPlayer(NamedPlayerMixin, BoardPlayerMixin):
    def play(self):
        super().play()

        try:
            x, y = str(input("Please enter coords to update the board? [x,y] ")).split(',')
            game.execute_move(self, int(x), int(y))
            print("\n")
        except Exception as e:
            print("{}\n".format(e))
            self.play()


game = ReversiGame()
players = (DemoCliPlayer(name="W", board=game.board),)

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (AIPlayer(name="B", board=game.board, game=game),)
else:
    players += (DemoCliPlayer(name="B", board=game.board),)

game.set_players(players)
print(game.get_legal_moves(players[0]))
game.play()
