
import json
import tornado.ioloop
import tornado.web
import tornado.websocket
import threading
import time

from gui.controller import GUIController


class WebsocketConnection(tornado.websocket.WebSocketHandler):
    """ Every new connection becomes an instance of this class """

    controller = None
    name = None

    def open(self, name):
        """ Method for a new connection. Subscribe to list. """
        RunServer.connection.append(self)
        self.controller = RunServer.get_client_player(name)

    def on_message(self, message):
        """ Method for an incomming message """
        self.controller.handle_message(message)

    def on_close(self):
        """ Method on closing the connection. Removes from list. """
        RunServer.connection.remove(self)
        if self.controller.nickname is not None:
            RunServer.inactive_clients[self.controller.nickname] = self

            lc = LoginChecker(self.controller.nickname)
            lc.start()

    def check_origin(self, origin):
        """ Method for connection handshake. """
        return True


class LoginChecker(threading.Thread):
    name = None

    def __init__(self, name_player):
        super().__init__()
        self.name = name_player

    def run(self):
        time.sleep(10)
        if self.name in RunServer.inactive_clients:
            RunServer.clients[self.name].handle_message('{"command":"logout"}')
            print("Logging out user: " + self.name)
            del RunServer.clients[self.name]
            del RunServer.inactive_clients[self.name]


class RunServer(threading.Thread):
    """ This is the class that runs the server and pushes messages. """

    # The array that will hold all the active connections
    connection = []
    clients = {}
    inactive_clients = {}
    instance = None

    @staticmethod
    def set_instance(rs):
        RunServer.instance = rs

    @staticmethod
    def get_instance():
        return RunServer.instance

    @staticmethod
    def get_client_player(name):
        if name in RunServer.clients and name != "":
            if name in RunServer.inactive_clients:
                del RunServer.inactive_clients[name]
            return RunServer.clients[name]
        else:
            pl = GUIController(RunServer.get_instance())
            if name is not "":
                RunServer.clients[name] = pl
            return pl

    @staticmethod
    def set_client_player(player, name):
        RunServer.clients[name] = player

    @staticmethod
    def run():
        """ This method will start the thread and sets up the server """
        app = tornado.web.Application([(r"/(.*)", WebsocketConnection)])
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

    @staticmethod
    def send_to_client(data):
        """ This method allows you to send messages to all subscribers """
        if(len(RunServer.connection) > 0):
            for singleServer in RunServer.connection:
                singleServer.write_message(data)
