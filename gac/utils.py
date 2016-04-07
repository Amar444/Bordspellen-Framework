""" All kinds of utilities """
from threading import Thread, Lock

from pyparsing import *


class Best(object):
    def __init__(self, v: any, r=0, c=0):
        """ Holds the best move"""
        # value of move
        self.val = v
        # row of move
        self.row = r
        # column of move
        self.column = c


class EventEmitter(object):
    def __init__(self):
        self.listeners_lock = Lock()
        self.listeners = {}

    def emit_event(self, event_name, data=None):
        """ Emits an event to all listening handlers """
        if event_name in self.listeners:
            for handler in self.listeners[event_name]:
                try:
                    Thread(target=handler, args=(data,)).run()
                except Exception as e:
                    print("Could not emit event {} to one of the listeners due to: {}".format(event_name, e))

    def on(self, event_name, handler):
        """ Subscribe for a specific event """
        with self.listeners_lock:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(handler)

    def off(self, event_name, handler=None):
        """ Unsubscribe for a specific event """
        with self.listeners_lock:
            if event_name in self.listeners:
                if handler is None:
                    self.listeners[event_name] = []
                elif handler in self.listeners[event_name]:
                    self.listeners[event_name].remove(handler)


def convert_values(s, l, tokens):
    n = tokens[0]
    try:
        return int(n)
    except ValueError:
        return n


def convert_fakeson(l):
    if type(l) == ParseResults:
        if l.haskeys():
            return l.asDict()
        return l.asList()
    return l


def parse_fakeson(data):
    l = fakesonParser.parseString(data)
    return [convert_fakeson(item) for item in l]


fakesonStringValue = Word(alphas + "_") | dblQuotedString.setParseAction(removeQuotes)
fakesonStringValue.setParseAction(convert_values)

fakesonArrayValues = delimitedList(fakesonStringValue)
fakesonArray = Suppress('[') + Optional(fakesonArrayValues) + Suppress(']')

fakesonKeypairValue = Group(Word(alphas + "_") + Suppress(Literal(':')) + fakesonStringValue)
fakesonObjectValues = delimitedList(fakesonKeypairValue)
fakesonObject = Dict(Suppress('{') + Optional(fakesonObjectValues) + Suppress('}'))

fakesonElements = Word(alphas) | Group(fakesonObject) | Group(fakesonArray)

fakesonParser = delimitedList(fakesonElements, delim=White(' ', exact=1))
