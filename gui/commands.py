from gui.controller import *

class Command:
    command = None
    controller = None
    client = None
    status = {
        'status': '',
        'message': ''
    }

    def __init__(self, controller, client):
        self.controller = controller
        self.client = client

    def send_to_server(self):
        self.client.on('OK', self.handle_ok)
        self.client.on('ERR', self.handle_err)

    def handle_ok(self, data):
        self.status['status'] = 'success'

    def handle_err(self, data):
        self.status['status'] = 'error'
        self.status['message'] = data[0]

    def destroy(self):
        self.client.off('OK', self.handle_ok)
        self.client.off('ERR', self.handle_err)


class CommandLogin(Command):
    command = 'login'

    nickname = None

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.nickname = message['nickname']
        self.connect_to_server('82.72.96.63', 7789)

    def connect_to_server(self, ip, port):
        self.client.on(EVENT_CONNECTED, self.send_to_server)
        self.client.on(EVENT_CONNECT_ERR, self.handle_err)
        self.client.connect((ip, port))

    def send_to_server(self, data):
        super().send_to_server()
        self.client.send(OutgoingCommand('LOGIN', self.nickname))
        self.handle_ok('your data')

    def handle_ok(self, data):
        super().handle_ok(data)
        self.controller.gui.set_client_player(self.controller, self.nickname)
        self.send_to_gui(self.nickname)
        self.destroy()

    def handle_err(self, data):
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def send_to_gui(self, nickname):
        self.controller.nickname = nickname
        self.controller.send_to_gui('loginStatus', {'playerName': nickname}, self.status['status'], self.status['message'])


class CommandLogout(Command):
    command = 'logout'

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        super().send_to_server()
        self.client.send(OutgoingCommand('logout'))


class CommandPlayerlist(Command):
    command = 'playerlist'

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        super().send_to_server()
        self.client.on('SVR', self.handle_svr)
        self.client.send(OutgoingCommand('get', 'playerlist'))

    def handle_err(self, data):
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def handle_svr(self, data):
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self, players):
        self.controller.send_to_gui('playerList', {'players': players}, self.status['status'], self.status['message'])

    def destroy(self):
        super().destroy()
        self.client.off('SVR', self.handle_svr)


class CommandGamelist(Command):
    command = 'gamelist'

    def __init__(self, controller, client, message):
        super().__init__(controller, client)
        self.send_to_server()

    def send_to_server(self):
        super().send_to_server()
        self.client.on('SVR', self.handle_svr)
        self.client.send(OutgoingCommand('get', 'gamelist'))

    def handle_err(self, data):
        super().handle_err(data)
        self.send_to_gui('')
        self.destroy()

    def handle_svr(self, data):
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self, games):
        self.controller.send_to_gui('gameList', {'games': games}, self.status['status'], self.status['message'])

    def destroy(self):
        super().destroy()
        self.client.off('SVR', self.handle_svr)


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
                                         '"' + self.player + '"', '"' + self.game + '"', '"' + self.turntime + '"'),
                                         {'status': 'OK', 'message': ''})

    def handle_ok(self, data):
        super().handle_ok(data)
        self.send_to_gui('')

    def handle_err(self, data):
        super().handle_ok(data)
        self.send_to_gui('')
        self.destroy()

    def handle_svr(self, data):
        if data.arguments[0] == 'PLAYERLIST':
            self.send_to_gui(data.arguments[1])
            self.destroy()

    def send_to_gui(self, challenge):
        self.controller.send_to_gui('challenge', {'': challenge}, self.status['status'], self.status['message'])

    def destroy(self):
        super().destroy()
        self.client.off('SVR', self.handle_svr)
