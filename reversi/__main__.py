""" This class provides the setup for an ReversiGame"""

from game import ReversiGame
from ai import AIPlayer, DemoReversiPlayer

game = ReversiGame()
players = ()


answer = str(input("Would you like to play against the computer? y/n"))
if answer == "y":
    players += (DemoReversiPlayer(name="u", board=game.board),)
    players += (AIPlayer(game, name="c", board=game.board),)
else:
    players += (DemoReversiPlayer(name="1", board=game.board),)
    players += (DemoReversiPlayer(name="2", board=game.board),)

game.set_players(players)
game.play()