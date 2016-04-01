"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import socket
from threading import Thread
import sys

import time


class ServerConnection(object):
    """ Used for communicating between the server and the local application """

    DEFAULT_IP = "localhost"
    DEFAULT_PORT = 7789

    # Strings used for the communication protocol
    ARGUMENT_SEPARATOR = " "
    COMMAND_SEPARATOR = "\n"
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

    def __init__(self, listeners=None, ip=None):
        """ Initializes a new ServerConnection to a server at the ip """
        if ip is None:
            ip = self.DEFAULT_IP
        self.incoming = ""
        self.connection = socket.socket()
        self.connection.connect((ip, self.DEFAULT_PORT))
        self.action_listeners = listeners
        self.running = True
        thread = Thread(target=self.run)
        thread.start()

    def run(self):
        """
        This thread checks for incoming messages from the server
        WARNING: Calling this method directly will result in an infinite loop
        """
        while True:
            self.incoming += self.connection.recv(256).decode()
            if len(self.incoming) > 2:
                print(self.incoming)
                self.incoming = ""

    def send_move(self, move):
        """ Sends a move to the Server """
        self.connection.send((self.SEND_MOVE_STRING + self.ARGUMENT_SEPARATOR + move + self.COMMAND_SEPARATOR).encode())

    def login(self, name="GROUP7"):
        """ Registers the application on the server using the name: name"""
        self.connection.send((self.LOGIN + self.ARGUMENT_SEPARATOR + name + self.COMMAND_SEPARATOR).encode())

    def logout(self):
        self.connection.send((self.LOGOUT + self.COMMAND_SEPARATOR).encode())

    def get_gamelist(self):
        self.connection.send((self.GET + self.ARGUMENT_SEPARATOR + self.GAMELIST + self.COMMAND_SEPARATOR).encode())

    def get_playerlist(self):
        self.connection.send((self.GET + self.ARGUMENT_SEPARATOR + self.PLAYERLIST + self.COMMAND_SEPARATOR).encode())

    def subscribe(self, gametype):
        self.connection.send((self.SUBSCRIBE + self.ARGUMENT_SEPARATOR + gametype + self.COMMAND_SEPARATOR).encode())

    def unsubscribe(self):
        self.connection.send((self.UNSUBSCRIBE + self.COMMAND_SEPARATOR).encode())

    def forfeit(self):
        self.connection.send((self.FORFEIT + self.COMMAND_SEPARATOR).encode())

    def challenge_player(self, player_name, gametype):
        self.connection.send((self.CHALLENGE + self.ARGUMENT_SEPARATOR +
                             player_name + self.ARGUMENT_SEPARATOR + gametype + self.COMMAND_SEPARATOR).encode())

    def accept_challenge(self, challenge_number):
        self.connection.send((self.CHALLENGE + self.ARGUMENT_SEPARATOR + self.ACCEPT +
                             self.ARGUMENT_SEPARATOR + challenge_number + self.COMMAND_SEPARATOR).encode())

    def notify_listeners(self, message):
        for listener in self.action_listeners:
            listener.action_performed(message)

if __name__ == '__main__':
    s = ServerConnection()
    time.sleep(3)
    print(s.connection.getpeername())
    s.login("BIATCH")

