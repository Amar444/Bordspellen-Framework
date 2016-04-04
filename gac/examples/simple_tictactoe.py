"""
Demonstrates a basic TicTacToe-like game without any AI, but acts as an example
on how to use the basic Player and Board classes to create a basic game with just
a few lines of code.
"""


from games import *
from boards import TwoDimensionalBoard
from players import BoardPlayerMixin, NamedPlayerMixin


class DemoBoard(TwoDimensionalBoard):
    size = (10, 5)


class DemoPlayer(BoardPlayerMixin, NamedPlayerMixin):
    def play(self):
        super().play()

        try:
            x, y = input("Please enter coords to update the board? [x,y] ").split(',')
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
