from client import Client, EVENT_CONNECTED, OutgoingCommand
import time


class PlayerClient(Client):
    def __init__(self, nickname):
        super().__init__()
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname

    def on_connected(self, data):
        self.send(OutgoingCommand('LOGIN', self.nickname))


client = PlayerClient("Knarf")
client.connect(('82.72.96.63', 7789))
time.sleep(1)

client.send(OutgoingCommand('get playerlist'))
