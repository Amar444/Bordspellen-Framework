"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import json
import socket

from threading import Thread
from gac.exceptions import InvalidCommandException
from gac.utils import parse_fakeson


EVENT_CONNECTED = '_CONNECTED'
EVENT_CONNECT_ERR = '_CONNECT_ERR'


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

    def __init__(self):
        self.endpoint = ('localhost', 7789)
        self.thread = None
        self.running = False
        self.connection = None
        self.listeners = {}

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
            self._setup()
            self._listen()
        except Exception as e:
            self.emit(EVENT_CONNECT_ERR, e)
            print("Could not connect to {} on port {}".format(self.endpoint[0], self.endpoint[1]))

        self.running = False

    def _setup(self):
        # Connect to the remote server
        self.connection = socket.socket()
        self.connection.connect(self.endpoint)

        # Notify the console
        print("Connected to {} on port {}\n".format(self.endpoint[0], self.endpoint[1]))

    def _listen(self):
        # Process incoming commands
        ignore = -2
        for raw in self._readcmd():
            print("S:", raw)

            if ignore <= 0:  # ignore the welcome message
                ignore += 1
                if ignore == 0:
                    self.emit(EVENT_CONNECTED)
                continue

            # Try to parse the incoming commands and then emit them to all
            # listeners through the emit method
            try:
                cmd = IncomingCommand(raw)
                self.emit(cmd.command, cmd)
            except Exception as e:
                print("Could not process incoming command due to: {}", e)

    def _readcmd(self):
        """ Reads from the socket and yields all incoming data back to the caller """
        for line in self.connection.makefile('r'):
            yield line[:-1]

    def emit(self, event_name, data=None):
        """ Emits an event to all listening handlers """
        if event_name in self.listeners:
            for handler in self.listeners[event_name]:
                try:
                    Thread(target=handler, args=(data,)).run()
                except Exception as e:
                    print("Could not emit event {} to one of the listeners due to: {}".format(event_name, e))

    def on(self, event_name, handler):
        """ Subscribe for a specific event """
        # todo: make this thread safe!!!
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(handler)

    def on(self, event_name, handler):
        """ unSubscribe for a specific event """
        # todo: make this thread safe!!!
        if event_name in self.listeners and handler in self.listeners[event_name]:
            self.listeners[event_name].remove(handler)

    def send(self, command):
        """ Sends an OutgoingCommand instance into the server """
        message = "{}\n".format(command)
        print("C: {}".format(message)[:-1])
        self.connection.send(message.encode())

    def disconnect(self):
        self.connection.close()
        self.running = False
