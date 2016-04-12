import json
from gac.exceptions import InvalidCommandException
from gac.utils import parse_fakeson


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

    def __str__(self):
        return 'OK'


class ErrCommand(BaseCommand):
    type = 'ERR'

    def __init__(self, details):
        self.arguments = [details]

    def __str__(self):
        return 'ERR {}'.format(self.arguments[0])
