"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import json
import socket
import time

from threading import Thread
from exceptions import InvalidCommandException

class BaseCommand(object):
    """ Represents the base class for an incoming or outgoing command """

    command = None
    arguments = None

    def __str__(self):
        """ Serializes the command into a string """
        if self.arguments is not None:
            arguments = self.arguments
            if isinstance(arguments, (tuple, dict, list)):
                arguments = json.dumps(self.arguments)
            return "{} {}".format(self.command, arguments)
        return self.command

    @property
    def has_arguments(self):
        """ Returns whether any arguments have been set """
        return self.arguments is not None


class OutgoingCommand(BaseCommand):
    """ Represents a outgoing command """

    command = None
    arguments = None

    def __init__(self, command: str, arguments: any=None):
        """ Initializes a new command """
        self.command = command
        self.arguments = arguments


class IncomingCommand(BaseCommand):
    """ Represents an incoming command """

    command = None
    arguments = None

    def __init__(self, raw: str):
        """ Initializes a new command by parsing the incoming string """
        try:
            splits = raw.split(' ', 1)
            self.command, self.arguments = splits if len(splits) == 2 else (splits[0], None)
        except Exception as e:
            raise InvalidCommandException(e.message)


class Client(object):
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
    PLAYERLIST = "playerlist"  # Using lowercase because of a mistake in the server implementation.
    SUBSCRIBE = "SUBSCRIBE"
    UNSUBSCRIBE = "UNSUBSCRIBE"
    FORFEIT = "FORFEIT"
    CHALLENGE = "CHALLENGE"
    ACCEPT = "ACCEPT"

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
            self.incoming = self.connection.recv(256).decode()
            while self.incoming[len(self.incoming) - 1] == self.COMMAND_SEPARATOR or \
                            self.incoming[len(self.incoming) - 1] == self.ARGUMENT_SEPARATOR:
                self.incoming = self.incoming[:-1]
            self.incoming = self.incoming[:-1]
            if self.incoming == self.ACKNOWLEDGEMENT:
                print("found an OK")
            else:
                print(self.incoming)
                self.notify_listeners(self.incoming)
            self.incoming = ""

    def send_move(self, move):
        """ Sends a move to the Server """
        self.connection.send((self.SEND_MOVE_STRING + self.ARGUMENT_SEPARATOR + move + self.COMMAND_SEPARATOR).encode())

    def login(self, name="GROUP7"):
        """ Registers the application on the server using the name: name"""
        self.connection.send((self.LOGIN + self.ARGUMENT_SEPARATOR + name + self.COMMAND_SEPARATOR).encode())

    def logout(self):
        """ Unregisters the application from the server"""
        self.connection.send((self.LOGOUT + self.COMMAND_SEPARATOR).encode())

    def get_gamelist(self):
        """ Request a list of avaiable gametypes from the server"""
        self.connection.send((self.GET + self.ARGUMENT_SEPARATOR + self.GAMELIST + self.COMMAND_SEPARATOR).encode())

    def get_playerlist(self):
        """ Request a list of logged in players from the server"""
        self.connection.send((self.GET + self.ARGUMENT_SEPARATOR + self.PLAYERLIST + self.COMMAND_SEPARATOR).encode())

    def subscribe(self, gametype):
        """ Subscribe for a tournament on the server """
        self.connection.send((self.SUBSCRIBE + self.ARGUMENT_SEPARATOR + gametype + self.COMMAND_SEPARATOR).encode())

    def unsubscribe(self):
        """ Unsubscribe from any tournament on the server"""
        self.connection.send((self.UNSUBSCRIBE + self.COMMAND_SEPARATOR).encode())

    def forfeit(self):
        """ Give up the curren match """
        self.connection.send((self.FORFEIT + self.COMMAND_SEPARATOR).encode())

    def challenge_player(self, player_name, gametype):
        """ Challenge an opponent to a game of gametype"""
        self.connection.send((self.CHALLENGE + self.ARGUMENT_SEPARATOR +
                              player_name + self.ARGUMENT_SEPARATOR + gametype + self.COMMAND_SEPARATOR).encode())

    def accept_challenge(self, challenge_number):
        """ Accept a challenge send by an opponent"""
        self.connection.send((self.CHALLENGE + self.ARGUMENT_SEPARATOR + self.ACCEPT +
                              self.ARGUMENT_SEPARATOR + challenge_number + self.COMMAND_SEPARATOR).encode())

    def notify_listeners(self, message):
        if self.action_listeners is not None:
            for listener in self.action_listeners:
                listener.action_performed(message)
        else:
            print("No listeners attached to this connection.")


if __name__ == '__main__':
    s = ServerConnection()
    time.sleep(3)
    print(s.connection.getpeername())
    s.login("BIATCH")
    s.get_gamelist()
    s.get_playerlist()
