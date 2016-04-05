from client import Client, EVENT_CONNECTED, OutgoingCommand
from tictactoe.game import TicTacToeGame
from tictactoe.tictactoe_players import CommandLinePlayer, ClientInputPlayer

game = TicTacToeGame()
client = Client()
client.on(EVENT_CONNECTED, client.on_connected)


def on_connected(self, data):
    self.send(OutgoingCommand('LOGIN', self.nickname))

"""
class PlayerClient(Client):
    def __init__(self, nickname):
        super().__init__()
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname

    def on_connected(self, data):
        self.send(OutgoingCommand('LOGIN', self.nickname))


PlayerClient("Knarf").connect()

game = TicTacToeGame()
players = (
    CommandLinePlayer(name="Frank", board=game.board),
    ClientInputPlayer(name="Knarf", board=game.board),
)
game.set_players(players)
game.play()
"""
