from game import TicTacToeGame
from ai import AIPlayer
import time

start = time.time()

game = TicTacToeGame()
game.set_players((AIPlayer(name="X", board=game.board, game=game),
                  AIPlayer(name="O", board=game.board, game=game),))
game.play()

end = time.time()

print("AI vs AI finished in {} ms.".format(end-start))