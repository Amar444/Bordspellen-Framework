from game import TicTacToeGame
from ai import AIPlayer, DemoTicTacToePlayer


game = TicTacToeGame()
players = ()

answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (DemoTicTacToePlayer(name="user", board=game.board),)
    players += (AIPlayer(game, name="computer", board=game.board),)
else:
    players += (DemoTicTacToePlayer(name="user 1", board=game.board),)
    players += (DemoTicTacToePlayer(name="user 2", board=game.board),)

game.set_players(players)
game.play()
