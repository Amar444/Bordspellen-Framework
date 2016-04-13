"""
Provides classes for every implemented command that the GUI wants to do.
"""

from gac.client.client import *


class Command:
    """ The super class of all commands. """
    command = None # command from the GUI that a command listens to, should be overwritten
    controller = None
    client = None
    status = {
        'status': '',
        'message': ''
    }

    def __init__(self, controller, client):
        """
        Initializes a command by letting it know of the controller that is using it and the client the command
        should communicate with
        """
        self.controller = controller
        self.client = client

    def send_to_server(self, *args):
        """
        'subscribes' to the OK and ERR reaction from the server. Every command send to the server will reply
        one of these
        """
        self.client.send(OutgoingCommand(*args), success=self.handle_ok, fail=self.handle_err)

    def handle_ok(self, data):
        """ sets the status if the server reaction was OK """
        self.status['status'] = 'success'
        self.status['message'] = ''

    def handle_err(self, data):
        """ sets the status if the server reaction was ERR """
        self.status['status'] = 'error'
        self.status['message'] = 'can\'t retrieve error message because of a bug in the fakeson parser.'


class CommandLogin(Command):
    """ Command to login to the game server. Creates a connection and then logs in. """
    command = 'login'

    nickname = None

    def __init__(self, controller, client, message):
        """ initializes a command to login """
        super().__init__(controller, client)
        self.nickname = message['nickname']
        self.connect_to_server(message['IP'], message['port'])

    def connect_to_server(self, ip, port):
        """ connects to a server with the given IP and port """
        self.client.on(EVENT_CONNECTED, self.send_to_server)
        self.client.on(EVENT_CONNECT_ERR, self.handle_err)
        self.client.connect((ip, port))

    def send_to_server(self, data):
        """ sends the login command to the server and calls the method that handles the OK 'subscription' """
        super().send_to_server('login', self.nickname)

    def handle_ok(self, data):
        """ if the login was successful, tell the GUI """
        super().handle_ok(data)
        self.controller.gui.set_client_player(self.controller, self.nickname)
        self.send_to_gui(self.nickname)

    def handle_err(self, data):
        """ if the connection to the server cannot be made or the login was not successful, tell the GUI """
        super().handle_err(data)
        self.send_to_gui('')

    def send_to_gui(self, nickname):
        """ send a message to the GUI """
        self.controller.nickname = nickname
        self.controller.start_listeners()
        self.controller.send_to_gui('loginStatus', {'playerName': nickname}, self.status['status'], self.status['message'])


class CommandLogout(Command):
    """ Command to logout from the server. """
    command = 'logout'

    def __init__(self, controller, client, message):
        """ initializes a command to logout """
        super().__init__(controller, client)
        super().send_to_server('logout')


class CommandPlayerlist(Command):
    """ Command to retreive the playerlist from the server. """
    command = 'playerlist'

    def __init__(self, controller, client, message):
        """ initializes a command to retreive the playerlist """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to retreive the playerlist, 'subscribes' to SVR to catch the response """
        self.client.on('PLAYERLIST', self.handle_svr)
        super().send_to_server('get', 'playerlist')

    def handle_err(self, data):
        """ if an error occurred send a response to the GUI """
        super().handle_err(data)
        self.send_to_gui('')

    def handle_svr(self, data):
        """ handle the reaction from the server """
        self.send_to_gui(data.arguments[0])

    def send_to_gui(self, players):
        """ send the playerlist to the GUI """
        self.controller.send_to_gui('playerList', {'players': players}, self.status['status'], self.status['message'])
        self.client.off('PLAYERLIST', self.handle_svr)


class CommandGamelist(Command):
    """ Command to retreive the gamelist from the server """
    command = 'gamelist'

    def __init__(self, controller, client, message):
        """ initializes a command to retreive the gamelist """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to retreive the gamelist, 'subscribes' to SVR to catch the response """
        self.client.on('GAMELIST', self.handle_svr)
        super().send_to_server('get', 'gamelist')

    def handle_err(self, data):
        """ if an error occurred send a response to the GUI """
        super().handle_err(data)
        self.send_to_gui('')

    def handle_svr(self, data):
        """ handle the reaction from the server """
        self.send_to_gui(data.arguments[0])

    def send_to_gui(self, games):
        """ send the gamelist to the GUI """
        self.controller.send_to_gui('gameList', {'games': games}, self.status['status'], self.status['message'])
        self.client.off('GAMELIST', self.handle_svr)


class CommandCreateChallenge(Command):
    """ Command to create a challenge """
    command = 'challenge'

    player = None
    game = None
    turntime = None
    play_as = None

    def __init__(self, controller, client, message):
        """ Initializes a command to challenge someone """
        super().__init__(controller, client)
        self.player = message['playername']
        self.game = message['gamename']
        self.turntime = message['turntime']
        self.play_as = message['playAs']
        self.send_to_server()

    def send_to_server(self):
        """ send the challenge to the server """
        super().send_to_server('challenge', '"' + self.player + '"', '"' + self.game + '"', self.turntime)

    def handle_ok(self, data):
        """ if calling out the challenge succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.controller.challenges[self.player] = self.play_as
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred with creating a challenge send a response to the GUI """
        super().handle_err(data)
        self.send_to_gui()

    def send_to_gui(self):
        """ let the GUI know that the challenge has been send or not """
        self.controller.send_to_gui('challenge', {}, self.status['status'], self.status['message'])


class CommandAcceptChallenge(Command):
    """ Command to accept an incoming challenge """
    command = 'accept'

    challenge = None
    play_as = None
    opponent = None

    def __init__(self, controller, client, message):
        """ Initializes a command to accept a challenge """
        super().__init__(controller, client)
        self.challenge = message['challenge']
        self.play_as = message['playAs']
        self.opponent = message['opponent']
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to accept a challenge """
        super().send_to_server('challenge', 'accept', self.challenge)

    def handle_ok(self, data):
        """ if accepting the challenge succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.controller.challenges[self.opponent] = self.play_as
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred when accepting the challenge """
        super().handle_err(data)
        self.send_to_gui()

    def send_to_gui(self):
        """ let the GUI know that accepting the challenge succeeded or not """
        self.controller.send_to_gui('accept', {}, self.status['status'], self.status['message'])


class CommandSubscribe(Command):
    """ Command to subscribe on a game """
    command = 'subscribe'

    game = None

    def __init__(self, controller, client, message):
        """ Initializes a command to subscribe to a game """
        super().__init__(controller, client)
        self.game = message['game']
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to subscribe to a game """
        super().send_to_server('subscribe', self.game)

    def handle_ok(self, data):
        """ if subscribing to the game succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred when subscribing to the game """
        super().handle_err(data)
        self.send_to_gui()

    def send_to_gui(self):
        """ let the GUI know that subscribing to the game succeeded or not """
        self.controller.send_to_gui('subscribe', {}, self.status['status'], self.status['message'])


class CommandUnsubscribe(Command):
    """ Command to unsubscribe """
    command = 'unsubscribe'

    def __init__(self, controller, client, message):
        """ Initializes a command to unsubscribe """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to unsubscribe """
        super().send_to_server('unsubscribe')

    def handle_ok(self, data):
        """ if unsubscribing succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred when unsubscribing """
        super().handle_err(data)
        self.send_to_gui()

    def send_to_gui(self):
        """ let the GUI know that unsubscribing succeeded or not """
        self.controller.send_to_gui('unsubscribe', {}, self.status['status'], self.status['message'])


class CommandMove(Command):
    command = 'move'

    x = None
    y = None

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.x = message['moveX']
        self.y = message['moveY']
        self.handle_move(self.x, self.y)

    def handle_move(self, x, y):
        try:
            self.controller.own_player.board.is_available(int(self.x), int(self.y))
            self.send_to_server()
        except Exception as e:
            self.handle_err('')

    def send_to_server(self):
        move = int(self.x) * int(self.controller.own_player.board.size[0])
        move += int(self.y) % int(self.controller.own_player.board.size[1])
        super().send_to_server('move', str(move))

    def handle_ok(self, data):
        super().handle_ok(data)
        self.controller.own_player.board.set(int(self.x), int(self.y), self.controller.own_player)
        self.send_to_gui()

    def handle_err(self, data):
        super().handle_err(data)
        self.status['message'] = 'move not valid'
        self.send_to_gui()

    def send_to_gui(self):
        self.controller.send_to_gui('moveListener', {}, self.status['status'], self.status['message'])
