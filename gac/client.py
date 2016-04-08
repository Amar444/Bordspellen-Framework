"""
Provides connection classes for use in communicating between the server and the local application
Might contain the connections between the local application and the GUI later
"""

import json
import socket

from threading import Thread, Lock
from exceptions import InvalidCommandException
from utils import parse_fakeson, EventEmitter

EVENT_CONNECTED = '_CONNECTED'
EVENT_CONNECT_ERR = '_CONNECT_ERR'
EVENT_GAME = 'GAME'


class BaseCommand(object):
    """ Represents the base class for an incoming or outgoing command """

    type = None
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
            self.type = parsed[0]
            if len(parsed) > 1:
                self.command = parsed[1]
                if len(parsed) > 2:
                    self.arguments = parsed[2:]
        except Exception as e:
            raise InvalidCommandException(e)

    def __str__(self):
        """ Returns the original, raw command """
        return self.raw


class OkCommand(BaseCommand):
    type = 'OK'


class ErrCommand(BaseCommand):
    type = 'ERR'

    def __init__(self, details):
        self.arguments = [details]


class Client(EventEmitter):
    """ Used for communicating between the server and the local application """


    def __init__(self):
        super().__init__()
        self.endpoint = ('localhost', 7789)
        self.thread = None
        self.running = False
        self.connection = None

        self._sync_event = None
        self._send_lock = Lock()

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
            self.emit_event(EVENT_CONNECT_ERR, e)
            print("Could not connect to {} on port {}".format(self.endpoint[0], self.endpoint[1]))

        self.running = False

    def _setup(self):
        """ Sets up the initial connection the the remote server """
        with self._send_lock:
            # Connect to the remote server
            self.connection = socket.socket()
            self.connection.connect(self.endpoint)

            # Notify the console
            print("Connected to {} on port {}\n".format(self.endpoint[0], self.endpoint[1]))

    def _listen(self):
        """ Listen for incoming commands and emit them through the EventEmitter """
        # Process incoming commands
        ignore = -2
        for raw in self._readcmd():
            print("S:", raw)

            if ignore < 0:  # ignore the welcome message
                ignore += 1
                if ignore == 0:
                    self.emit_event(EVENT_CONNECTED)
                continue

            # Try to parse the incoming commands and then emit them to all
            # listeners through the emit method
            try:
                if raw == 'OK':
                    self.emit_event('OK', OkCommand())
                elif len(raw) >= 3 and raw[:3] == 'ERR':
                    self.emit_event('ERR', ErrCommand(raw[:3]))
                else:
                    cmd = IncomingCommand(raw)
                    self.emit_event(cmd.command, cmd)
            except Exception as e:
                print("Could not process incoming command due to: {}", e)

    def _readcmd(self):
        """ Reads from the socket and yields all incoming data back to the caller """
        for line in self.connection.makefile('r'):
            yield line[:-1]

    def send_sync(self, command: OutgoingCommand):
        lock = Lock()
        lock.acquire()

        def callback(e):
            self._sync_event = e
            lock.release()

        self.send(command, success=callback, fail=callback)

        lock.acquire()
        lock.release()

        return self._sync_event

    def send(self, command: OutgoingCommand, success: callable=None, fail: callable=None):
        """ Sends an OutgoingCommand instance into the server """
        self._send_lock.acquire()
        print("C:", command)

        message = "{}\n".format(command)
        self.connection.send(message.encode())

        if not success and not fail:
            self._send_lock.release()
        else:
            def callback(method):
                def hook(cmd):
                    self._send_lock.release()
                    self.off('OK')
                    self.off('ERR')
                    method(cmd)
                return hook

            if success:
                self.on('OK', callback(success))

            if fail:
                self.on('ERR', callback(fail))

    def disconnect(self):
        """ Disconnect from the remote server """
        print("Disconnecting from {} on port {}".format(self.endpoint[0], self.endpoint[1]))
        self.connection.close()
        self.running = False