import sys
"""y u no recognize numpy """
sys.path.append("/usr/local/lib/python3.4/dist-packages/")
import time
from game import ReversiGame
from ai import AIPlayer

start = time.time()

game = ReversiGame()
game.set_players((AIPlayer(name="W", board=game.board, game=game),
                  AIPlayer(name="B", board=game.board, game=game),))
for player in game.players:
    player.print_board = False
game.play()

end = time.time()

print("AI vs AI finished in {} s.".format(end-start))