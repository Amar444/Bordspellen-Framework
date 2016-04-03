""" All kinds of utilities """

from pyparsing import *

def convertValues(s, l, tokens):
    n = tokens[0]
    try:
        return int(n)
    except:
        return n


fakesonStringValue = Word(alphas + "_") | dblQuotedString.setParseAction(removeQuotes)
fakesonStringValue.setParseAction(convertValues)

fakesonArrayValues = delimitedList(fakesonStringValue)
fakesonArray = Suppress('[') + Optional(fakesonArrayValues) + Suppress(']')

fakesonKeypairValue = Group(Word(alphas + "_") + Suppress(':') + fakesonStringValue)
fakesonObjectValues = delimitedList(fakesonKeypairValue)
fakesonObject = Dict(Suppress('{') + Optional(fakesonObjectValues) + Suppress('}'))

fakesonElements = Word(alphas) | Group(fakesonObject) | Group(fakesonArray)

fakesonParser = delimitedList(fakesonElements, delim=White(' ', exact=1))

def parse_fakeson(data):
    return fakesonParser.parseString(data).asList()
