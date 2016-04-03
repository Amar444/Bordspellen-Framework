from game import TicTacToeGame
from ai import AIPlayer
from players import NamedPlayerMixin, Player, BoardPlayerMixin


class TicTacToeDemoPlayerMixin(Player):
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


class DemoAiPlayer(AIPlayer, TicTacToeDemoPlayerMixin):
    pass


class DemoCliPlayer(BoardPlayerMixin, NamedPlayerMixin, TicTacToeDemoPlayerMixin):
    pass


game = TicTacToeGame()
players = ()

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (DemoCliPlayer(name="u", board=game.board),)
    players += (DemoAiPlayer(game, name="c", board=game.board),)
else:
    players += (DemoCliPlayer(name="1", board=game.board),)
    players += (DemoCliPlayer(name="2", board=game.board),)

game.set_players(players)
game.play()
