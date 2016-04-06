""" All kinds of utilities """

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
