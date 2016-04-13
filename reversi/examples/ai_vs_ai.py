import time
from game import ReversiGame
from ai import ReversiAIPlayer

start = time.time()

game = ReversiGame()


game.set_players((ReversiAIPlayer(name="W", game=game),
                  ReversiAIPlayer(name="B", game=game),))
for player in game.players:
    player.print_board = False

game.play()

end = time.time()

print("AI vs AI finished in {} s.".format(end-start))