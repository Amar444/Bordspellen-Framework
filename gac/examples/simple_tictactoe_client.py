from client import Client, EVENT_CONNECTED, OutgoingCommand
from tictactoe.game import TicTacToeGame
from tictactoe.tictactoe_players import CommandLinePlayer, ClientInputPlayer
import time


class PlayerClient(Client):
    def __init__(self, nickname):
        super().__init__()
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname

    def on_connected(self, data):
        self.send(OutgoingCommand('LOGIN', self.nickname))

    def on_OK(self, data):
        print(data)


client = PlayerClient("Knarf")
client.connect()
time.sleep(1)
client.on('OK', client.on_OK)

client.send(OutgoingCommand('get gamelist'))
