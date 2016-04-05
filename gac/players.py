"""
Provides implementation for Player objects
"""

from gac.client import *
import json

class Player(object):
    """ Player is used to define a player in the game """

    def play(self):
        """ It is your turn, play the game """
        pass


class BoardPlayerMixin(Player):
    """ Player mixin that supports having a board """

    board = None
    print_board = True

    def __init__(self, board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board

    def play(self):
        """ Prints the board to the console while playing if enabled """
        if self.print_board:
            print(self.board)
        super().play()


class NamedPlayerMixin(Player):
    """ Player mixin that supports having a name """

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name or 'Unknown'

    def play(self):
        """ It is your turn, play the game """
        print(self.name, "is now playing.")
        super().play()

    def __str__(self):
        """ Returns the current player name """
        return self.name


class ClientPlayerMixin(Player):
    """ Player mixin that supports input from a server """

    client = None
    lastMove = None

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        client.on("SRV", self.handle_move)

    def handle_command(self, command):
        """ handles a command passed from the client, handling needs to be specified by siblings of this class """
        pass


class ClientPlayer(Client):
    run_server = None

    def __init__(self, run_server):
        super().__init__()
        self.run_server = run_server

    def handle_message(self, message):
        action = str.split(message)[0]

        if action == 'login':
            self.login(str.split(message)[1])
        else:
            print(message)

    def login(self, nickname):
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname
        self.connect(('82.72.96.63', 7789))

    def on_connected(self, data):
        self.on('OK', self.login_success)
        self.on('ERR', self.login_failed)
        self.send(OutgoingCommand('LOGIN', self.nickname))
        self.run_server.sendToClient(json.dumps(
            {
                'listener': 'loginStatus',
                'detail': {
                    'status': 'success',
                    'playerName': self.nickname
                }
            }
        ))

    def login_success(self, data):
        print("i received OK")
        self.run_server.sendToClient(json.dumps(
            {
                'listener': 'loginStatus',
                'detail': {
                    'status': 'success',
                    'playerName': self.nickname
                }
            }
        ))

    def login_failed(self, data):
        print("i received ERR")
        self.run_server.sendToClient(json.dumps(
            {
                'listener': 'loginStatus',
                'detail': {
                    'status': 'failed',
                    'playerName': self.nickname
                }
            }
        ))