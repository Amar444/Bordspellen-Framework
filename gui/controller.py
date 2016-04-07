from gac.client import *
import json

"""
NOTE:
this is the beginning of the much needed refactor. What still needs to be done before it can be reviewed:
- Add comments/documentation
- implement the OK and ERR response from the server
- maybe create a class that represents the get and send command for everye command (get_playerlist, get_gamelist,
send_playerlist, send_gamelist). But this will be decided once the OK and ERR responses are implemented
"""


class GUIController:
    gui = None
    client = None

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.client = Client()

    def handle_message(self, message):
        message = self.handle_json(message)

        try:
            command = message['command']
        except Exception as e:
            print("JSON does not contain a command")
            command = 'No command found'

        if command == 'login':
            self.login(message['nickname'])
        elif command == 'playerlist':
            self.get_playerlist()
        elif command == 'gamelist':
            self.get_gamelist()
        else:
            print("Command not recognized. Command: " + command)

    def handle_json(self, json_str):
        try:
            json_str = json.loads(str(json_str))
        except Exception as e:
            json_str = None
            print("Could not convert JSON, exception: {}", e)
        return json_str

    def login(self, nickname):
        self.client.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname
        self.client.connect(('82.72.96.63', 7789))

    def on_connected(self, data):
        self.client.send(OutgoingCommand('LOGIN', self.nickname))

        self.client.on('SVR', self.handle_svr)
        self.gui.set_client_player(self, self.nickname)
        self.gui.send_to_client(json.dumps(
            {
                'listener': 'loginStatus',
                'detail': {
                    'status': 'success',
                    'playerName': self.nickname
                }
            }
        ))

    def handle_svr(self, data):
        value = data.arguments[0]
        if value == 'PLAYERLIST':
            self.send_playerlist(data.arguments[1])
        elif value == 'GAMELIST':
            self.send_gamelist(data.arguments[1])
        else:
            print("Return value not recognized. Value: " + value)

    def send_to_gui(self, listener, details):
        self.gui.send_to_client(json.dumps(
            {
                'listener': listener,
                'detail': details,
                'status': {
                    'status': 'OK',
                    'message': ''
                }
            }
        ))

    def get_playerlist(self):
        self.client.send(OutgoingCommand('get playerlist'))

    def send_playerlist(self, playerlist):
        self.send_to_gui('playerList', {'players': playerlist})

    def get_gamelist(self):
        self.client.send(OutgoingCommand('get gamelist'))

    def send_gamelist(self, gamelist):
        self.send_to_gui('gameList', {'games': gamelist})
