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

    def __init__(self):
        super().__init__()

        player1 = input("First player name:  ")
        player2 = input("Second player name: ")

        self.set_players((DemoPlayer(name=player1, board=self.board),
                          DemoPlayer(name=player2, board=self.board)))


game = DemoGame()
game.play()
