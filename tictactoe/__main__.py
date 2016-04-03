from game import TicTacToeGame
from ai import AIPlayer
from players import Player, BoardPlayerMixin, NamedPlayerMixin


class DemoCliPlayer(NamedPlayerMixin, BoardPlayerMixin, Player):
    def play(self):
        super().play()

        try:
            x, y = str(input("Please enter coords to update the board? [x,y] ")).split(',')
            if self.board.is_available(int(x), int(y)):
                self.board.set(int(x), int(y), self)
            else:
                raise Exception("The given coords are not available on the current board")
            print("\n")
        except Exception as e:
            print("{}\n".format(e))
            self.play()


game = TicTacToeGame()
players = (DemoCliPlayer(name="X", board=game.board),)

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (AIPlayer(name="O", board=game.board, game=game),)
else:
    players += (AIPlayer(name="O", board=game.board),)

game.set_players(players)
game.play()
