from game import TicTacToeGame
from ai import AIPlayer
import time

start = time.time()

game = TicTacToeGame()
game.set_players((AIPlayer(name="X", game=game),
                  AIPlayer(name="O", game=game),))
game.play()

end = time.time()

print("AI vs AI finished in {} ms.".format(end-start))