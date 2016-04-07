"""
Provides classes for every implemented command that the GUI wants to do.
"""

from gac.client import *


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

    def send_to_server(self):
        """
        'subscribes' to the OK and ERR reaction from the server. Every command send to the server will reply
        one of these
        """
        self.client.on('OK', self.handle_ok)
        self.client.on('ERR', self.handle_err)

    def handle_ok(self, data):
        """ sets the status if the server reaction was OK """
        self.status['status'] = 'success'

    def handle_err(self, data):
        """ sets the status if the server reaction was ERR """
        self.status['status'] = 'error'
        self.status['message'] = data[0]

    def destroy(self):
        """
        should be called after a response is send to the GUI, 'unsubscribes' from the OK and ERR reaction of the server
        """
        self.client.off('OK', self.handle_ok)
        self.client.off('ERR', self.handle_err)


class CommandLogin(Command):
    """ Command to login to the game server. Creates a connection and then logs in. """
    command = 'login'

    nickname = None

    def __init__(self, controller, client, message):
        """ initializes a command to login """
        super().__init__(controller, client)
        self.nickname = message['nickname']
        self.connect_to_server('82.72.96.63', 7789)

    def connect_to_server(self, ip, port):
        """ connects to a server with the given IP and port """
        self.client.on(EVENT_CONNECTED, self.send_to_server)
        self.client.on(EVENT_CONNECT_ERR, self.handle_err)
        self.client.connect((ip, port))

    def send_to_server(self, data):
        """ sends the login command to the server and calls the method that handles the OK 'subscription' """
        super().send_to_server()
        self.client.send(OutgoingCommand('LOGIN', self.nickname))
        self.handle_ok('your data') # when 'subscribing' on OK and ERR after login works, this should be removed

    def handle_ok(self, data):
        """ if the login was successful, tell the GUI """
        super().handle_ok(data)
        self.controller.gui.set_client_player(self.controller, self.nickname)
        self.send_to_gui(self.nickname)
        self.destroy()

    def handle_err(self, data):
        """ if the connection to the server cannot be made or the login was not successful, tell the GUI """
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def send_to_gui(self, nickname):
        """ send a message to the GUI """
        self.controller.nickname = nickname
        self.controller.send_to_gui('loginStatus', {'playerName': nickname}, self.status['status'], self.status['message'])


class CommandLogout(Command):
    """ Command to logout from the server. """
    command = 'logout'

    def __init__(self, controller, client, message):
        """ initializes a command to logout """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ Logs out of the server """
        super().send_to_server()
        self.client.send(OutgoingCommand('logout'))


class CommandPlayerlist(Command):
    """ Command to retreive the playerlist from the server. """
    command = 'playerlist'

    def __init__(self, controller, client, message):
        """ initializes a command to retreive the playerlist """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to retreive the playerlist, 'subscribes' to SVR to catch the response """
        super().send_to_server()
        self.client.on('SVR', self.handle_svr)
        self.client.send(OutgoingCommand('get', 'playerlist'))

    def handle_err(self, data):
        """ if an error occurred send a response to the GUI """
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def handle_svr(self, data):
        """ handle the reaction from the server """
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self, players):
        """ send the playerlist to the GUI """
        self.controller.send_to_gui('playerList', {'players': players}, self.status['status'], self.status['message'])

    def destroy(self):
        """ 'unsubscibe' from the server command because we handled it, no need to stay informed about it """
        super().destroy()
        self.client.off('SVR', self.handle_svr)


class CommandGamelist(Command):
    """ Command to retreive the gamelist from the server """
    command = 'gamelist'

    def __init__(self, controller, client, message):
        """ initializes a command to retreive the gamelist """
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to retreive the gamelist, 'subscribes' to SVR to catch the response """
        super().send_to_server()
        self.client.on('SVR', self.handle_svr)
        self.client.send(OutgoingCommand('get', 'gamelist'))

    def handle_err(self, data):
        """ if an error occurred send a response to the GUI """
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def handle_svr(self, data):
        """ handle the reaction from the server """
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self, games):
        """ send the gamelist to the GUI """
        self.controller.send_to_gui('gameList', {'games': games}, self.status['status'], self.status['message'])

    def destroy(self):
        """ 'unsubscibe' from the server command because we handled it, no need to stay informed about it """
        super().destroy()
        self.client.off('SVR', self.handle_svr)


# NOTE: this command is not done yet!
class CommandCreateChallange(Command):
    command = 'challenge'

    player = None
    game = None
    turntime = None

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.player = message['playername']
        self.game = message['gamename']
        self.turntime = message['turntime']
        self.send_to_server()

    def send_to_server(self):
        super().send_to_server()
        self.client.on('SVR', self.handle_svr)
        self.client.send(OutgoingCommand('challenge',
                                         '"' + self.player + '"', '"' + self.game + '"', '"' + self.turntime + '"',
                                         {'status': 'OK', 'message': ''}))

    def handle_ok(self, data):
        """ if calling out the challenge succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred send a response to the GUI """
        super().handle_ok(data)
        self.send_to_gui()
        self.destroy()

    def handle_svr(self, data):
        """ note: to be implemented right """
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self):
        """ let the GUI know that the challenge has been send or not """
        self.controller.send_to_gui('challenge', {}, self.status['status'], self.status['message'])

    def destroy(self):
        """ 'unsubscibe' from the server command because we handled it, no need to stay informed about it """
        super().destroy()
        self.client.off('SVR', self.handle_svr)


class CommandAcceptChallange(Command):
    """ Command to accept an incoming challenge """
    command = 'accept'

    challenge = None

    def __init__(self, controller, client, message):
        """ Initializes a command to accept a challenge """
        super().__init__(controller, client)
        self.challenge = message['challenge']
        self.send_to_server()

    def send_to_server(self):
        """ sends a command to the server to accept a challenge """
        super().send_to_server()
        self.client.send(OutgoingCommand('challenge', 'accept', self.challenge))

    def handle_ok(self, data):
        """ if accepting the challenge succeeded, tell it to the GUI """
        super().handle_ok(data)
        self.send_to_gui()

    def handle_err(self, data):
        """ if an error occurred when accepting the challenge """
        super().handle_ok(data)
        self.send_to_gui()
        self.destroy()

    def send_to_gui(self):
        """ let the GUI know that accepting the challenge succeeded or not """
        self.controller.send_to_gui('challenge', {}, self.status['status'], self.status['message'])
