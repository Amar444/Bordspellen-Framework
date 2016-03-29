from games import *
from boards import TwoDimensionalBoard
from players import BoardPlayerMixin, NamedPlayerMixin, CommandLineInputPlayerMixin

class DemoBoard(TwoDimensionalBoard):
    size = (10, 5)


class DemoPlayer(BoardPlayerMixin, NamedPlayerMixin, CommandLineInputPlayerMixin):
    def play(self):
        super().play()


class DemoGame(TurnBasedGame, BoardGame):
    board_class = DemoBoard


game = DemoGame()
players = ()

for x in range(0, int(input("How many players would you like to add? "))):
    player_name = input("Name for player {}?".format(x + 1))
    players += (DemoPlayer(name=player_name, board=game.board),)

game.set_players(players)
game.play()
