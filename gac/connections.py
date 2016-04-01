"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import socket
from threading import Thread


class ServerConnection(object):
    """ Used for communicating between the server and the local application """

    DEFAULT_IP = "localhost"
    DEFAULT_PORT = 7789

    # Strings used for the communication protocol
    ARGUMENT_SEPARATOR = " "
    COMMAND_SEPARATOR = "/n"  # not sure about this yet
    MAP_START = "{"
    MAP_END = "}"
    LIST_START = "["
    LIST_END = "]"

    ACKNOWLEDGEMENT = "OK"
    ERROR = "ERR"
    SERVER = "SVR"

    SEND_MOVE_STRING = "MOVE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    GET = "GET"
    GAMELIST = "GAMELIST"
    PLAYERLIST = "PLAYERLIST"
    SUBSCRIBE = "SUBSCRIBE"
    UNSUBSCRIBE = "UNSUBSCRIBE"
    FORFEIT = "FORFEIT"
    CHALLENGE = "CHALLENGE"
    ACCEPT = "ACCEPT"


    action_listeners = None

    def __init__(self, listeners, ip=None):
        """ Initializes a new ServerConnection to a server at the ip """
        if ip is None:
            ip = self.DEFAULT_IP
        self.connection = socket.create_connection((ip,self.DEFAULT_PORT))
        self.action_listeners = listeners
        thread = Thread(target=self.run())
        thread.start()

    def run(self):
        """
        This thread checks for incoming messages from the server
        WARNING: Calling this method directly will result in an infinite loop
        """
        while True:
            self.incoming += self.connection.recv(256)

    def send_move(self, move):
        """ Sends a move to the Server """
        self.connection.send(self.SEND_MOVE_STRING + self.ARGUMENT_SEPARATOR + move)

    def login(self, name = "GROUP7"):
        """ Registers the application on the server using the name: name"""
        self.connection.send(self.LOGIN + self.ARGUMENT_SEPARATOR + name)

    def logout(self):
        self.connection.send(self.LOGOUT)

    def get_gamelist(self):
        self.connection.send(self.GET + self.ARGUMENT_SEPARATOR + self.GAMELIST)

    def get_playerlist(self):
        self.connection.send(self.GET + self.ARGUMENT_SEPARATOR + self.PLAYERLIST)

    def subscribe(self, gametype):
        self.connection.send(self.SUBSCRIBE + self.ARGUMENT_SEPARATOR + gametype)

    def unsubscribe(self):
        self.connection.send(self.UNSUBSCRIBE)

    def forfeit(self):
        self.connection.send(self.FORFEIT)

    def challenge_player(self, player_name, gametype):
        self.connection.send(self.CHALLENGE + self.ARGUMENT_SEPARATOR
                             + player_name + self.ARGUMENT_SEPARATOR + gametype)

    def accept_challenge(self, challenge_number):
        self.connection.send(self.CHALLENGE + self.ARGUMENT_SEPARATOR + self.ACCEPT
                             + self.ARGUMENT_SEPARATOR + challenge_number)