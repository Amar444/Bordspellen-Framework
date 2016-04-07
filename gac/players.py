"""
Provides implementation for Player objects
"""

"""
NOTE

This file is far from finished and will be refactored a lot!
Currenlty I (Frank) am just implementing GUI interaction so the GUI team can also make great progress
This also includes copy-pasting functions and then changing minor things, of course in the future this will be
majesticly refactored! (don't know if majesticly is a word, but I like it)

refactoring will be done soon ;)

NOTE
"""

from gac.client import *
from gac.utils import *
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
            self.login(message[6:])
        elif action == 'playerlist':
            self.get_playerlist()
        elif action == 'gamelist':
            self.get_gamelist()
        else:
            print(message)

    def login(self, nickname):
        self.on(EVENT_CONNECTED, self.on_connected)
        self.nickname = nickname
        self.connect(('82.72.96.63', 7789))

    def on_connected(self, data):
        self.send(OutgoingCommand('LOGIN', self.nickname))
        self.on('SVR', self.send_playerlist)
        self.on('SVR', self.send_gamelist)

        self.run_server.setClientPlayer(self, self.nickname)
        self.run_server.sendToClient(json.dumps(
            {
                'listener': 'loginStatus',
                'detail': {
                    'status': 'success',
                    'playerName': self.nickname
                }
            }
        ))

    def get_playerlist(self):
        self.send(OutgoingCommand('get playerlist'))

    def send_playerlist(self, data):
        if data.arguments[0] == 'PLAYERLIST':
            players = data.raw[16:-1]
            players = players.replace('"', '')
            players = players.split(', ')

            self.run_server.sendToClient(json.dumps(
                {
                    'listener': 'playerList',
                    'detail': {
                        'players': players
                    }
                }
            ))

    def get_gamelist(self):
        self.send(OutgoingCommand('get gamelist'))

    def send_gamelist(self, data):
        if data.arguments[0] == 'GAMELIST':
            games = data.raw[14:-1]
            games = games.replace('"', '')
            games = games.split(', ')

            print(
                json.dumps(
                    {
                        'listener': 'gameList',
                        'detail': {
                            'games': games
                        }
                    }
                )
            )

            self.run_server.sendToClient(json.dumps(
                {
                    'listener': 'gameList',
                    'detail': {
                        'games': games
                    }
                }
            ))
