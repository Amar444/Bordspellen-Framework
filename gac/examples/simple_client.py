from time import sleep
from client import Client, EVENT_CONNECTED, OutgoingCommand

print("Warning: this will loop forever waiting for incoming messages")
print("from the server. You may want to stop this script using Ctrl-C")
print("")


class PlayerClient(Client):
    def __init__(self, nickname):
        super().__init__()
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname

    def on_connected(self, data):
        self.send(OutgoingCommand('LOGIN', self.nickname))


PlayerClient("Kwieb").connect()
PlayerClient("Robert").connect()