from game import TicTacToeGame
from ai import AIPlayer
from players import NamedPlayerMixin, Player, BoardPlayerMixin


class TicTacToeDemoPlayerMixin(BoardPlayerMixin, Player):
    def play(self):
        super().play()

        try:
            x, y = str(input("Please enter coords to update the board? [x,y] ")).split(',')
            self.board.set(int(x), int(y), self)
            print("\n")
        except Exception as e:
            print(e)
            self.play()


class DemoAiPlayer(AIPlayer, TicTacToeDemoPlayerMixin):
    pass


class DemoCliPlayer(NamedPlayerMixin, TicTacToeDemoPlayerMixin):
    pass


game = TicTacToeGame()
players = (DemoCliPlayer(name="X", board=game.board),)

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (DemoAiPlayer(name="O", board=game.board, game=game),)
else:
    players += (DemoCliPlayer(name="O", board=game.board),)

game.set_players(players)
game.play()
