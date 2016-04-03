"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import json
import socket
import time

from threading import Thread
from exceptions import InvalidCommandException
from utils import parse_fakeson


class BaseCommand(object):
    """ Represents the base class for an incoming or outgoing command """

    command = None
    arguments = None

    def __str__(self):
        """ Serializes the command into a string """
        if self.arguments is not None:
            arguments = []
            for arg in self.arguments:
                if isinstance(arg, str):
                    arguments.append(arg)
                elif isinstance(arg, (tuple, list)):
                    arguments.append(json.dumps(arg))
                elif isinstance(arg, dict):
                    buffer = '{'
                    for k, v in arg.items():
                        buffer += k + ': "' + v + "'"
                    buffer += '}'
                    arguments.append(buffer)
            return "{} {}".format(self.command, " ".join(arguments))
        return self.command

    @property
    def has_arguments(self):
        """ Returns whether any arguments have been set """
        return self.arguments is not None


class OutgoingCommand(BaseCommand):
    """ Represents a outgoing command """

    def __init__(self, command: str, *args):
        """ Initializes a new command """
        self.command = command
        if len(args) > 0:
            self.arguments = args


class IncomingCommand(BaseCommand):
    """ Represents an incoming command """

    raw = None

    def __init__(self, raw: str):
        """ Initializes a new command by parsing the incoming string """
        self.raw = raw
        try:
            parsed = parse_fakeson(raw)
            self.command = parsed[0]
            if len(parsed) > 1:
                self.arguments = parsed[1:]
        except Exception as e:
            raise InvalidCommandException(e)

    def __str__(self):
        """ Returns the original, raw command """
        return self.raw


class Client(object):
    """ Used for communicating between the server and the local application """

    endpoint = ('localhost', 7789)
    thread = None
    running = False
    connection = None
    ignored_messages = ('OK', 'ERR')
    subscriptions = {}

    def connect(self, endpoint=None):
        """ Initializes a new connection to a server at the specified endpoint """
        if endpoint is not None and len(endpoint) == 2:
            self.endpoint = endpoint

        self.thread = Thread(target=self._run)
        self.running = True
        self.thread.start()

    def _run(self):
        """ This thread checks for incoming messages from the server """

        try:
            # Connect to the remote server
            self.connection = socket.socket()
            self.connection.connect(self.endpoint)

            # Notify the console
            print("Connected to {} on port {}\n".format(self.endpoint[0], self.endpoint[1]))

            # Process incoming commands
            ignore = -2
            for cmd in self._readcmd():
                print("S:", cmd)

                if ignore <= 0:  # ignore the welcome message
                    ignore += 1
                    continue

                # todo: announce this as an event
                parsed_command = IncomingCommand(cmd)
                print(parsed_command)

        except:
            # todo: announce this as an event
            print("Could not connect to {} on port {}".format(self.endpoint[0], self.endpoint[1]))

        self.running = False

    def _readcmd(self):
        for line in self.connection.makefile('r'):
            if line[:-1] not in self.ignored_messages:
                yield line[:-1]

    # def notify_listeners(self, message):
    #     if self.action_listeners is not None:
    #         for listener in self.action_listeners:
    #             listener.action_performed(message)
    #     else:
    #         print("No listeners attached to this connection.")

    def disconnect(self):
        self.connection.close()
        self.running = False
