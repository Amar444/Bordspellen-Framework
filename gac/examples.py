from games import *
from boards import TwoDimensionalBoard
from players import BoardPlayerMixin, NamedPlayerMixin

class DemoBoard(TwoDimensionalBoard):
    size = (10, 5)


class DemoPlayer(BoardPlayerMixin, NamedPlayerMixin):
    def play(self):
        super().play()

        try:
            coords = input("Please enter coords to update the board? [x,y] ")
            x, y = coords.split(',')
            self.board.set(int(x), int(y), self.name[0:1])
            print("\n")
        except Exception as e:
            print(e)
            self.play()


class DemoGame(TurnBasedGame, BoardGame):
    board_class = DemoBoard


game = DemoGame()
players = ()

for x in range(0, int(input("How many players would you like to add? "))):
    player_name = input("Name for player {}?".format(x + 1))
    players += (DemoPlayer(name=player_name, board=game.board),)

game.set_players(players)
game.play()
