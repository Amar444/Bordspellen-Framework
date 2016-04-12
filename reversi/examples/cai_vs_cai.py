import time
from game import ReversiGame
from ai import AIPlayerC

start = time.time()

game = ReversiGame()
game.set_players((AIPlayerC(name="W", board=game.board, game=game),
                  AIPlayerC(name="B", board=game.board, game=game),))
game.play()

end = time.time()

print("AI vs AI finished in {} s.".format(end-start))