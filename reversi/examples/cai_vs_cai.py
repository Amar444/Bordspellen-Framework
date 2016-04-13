import sys
"""y u no recognize numpy """
sys.path.append("/usr/local/lib/python3.4/dist-packages/")
import time
from game import ReversiGame
from ai import AIPlayerC, ReversiAIPlayer

start = time.time()

game = ReversiGame()
game.set_players((AIPlayerC(name="W", game=game),
                  ReversiAIPlayer(name="B", game=game),))
for player in game.players:
    player.print_board = False

game.play()

end = time.time()

print("CAI vs CAI finished in {} s.".format(end-start))