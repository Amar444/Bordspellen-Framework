from game import TicTacToeGame
from ai import AIPlayer, DemoTicTacToePlayer


game = TicTacToeGame()
players = ()

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (DemoTicTacToePlayer(name="u", board=game.board),)
    players += (AIPlayer(game, name="c", board=game.board),)
else:
    players += (DemoTicTacToePlayer(name="1", board=game.board),)
    players += (DemoTicTacToePlayer(name="2", board=game.board),)

game.set_players(players)
game.play()
