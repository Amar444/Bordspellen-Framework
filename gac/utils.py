""" All kinds of utilities """

from pyparsing import *

def convert_values(s, l, tokens):
    n = tokens[0]
    try:
        return int(n)
    except:
        return n


fakesonStringValue = Word(alphas + "_") | dblQuotedString.setParseAction(removeQuotes)
fakesonStringValue.setParseAction(convert_values)

fakesonArrayValues = delimitedList(fakesonStringValue)
fakesonArray = Suppress('[') + Optional(fakesonArrayValues) + Suppress(']')

fakesonKeypairValue = Group(Word(alphas + "_") + Suppress(':') + fakesonStringValue)
fakesonObjectValues = delimitedList(fakesonKeypairValue)
fakesonObject = Dict(Suppress('{') + Optional(fakesonObjectValues) + Suppress('}'))

fakesonParser = fakesonObject | fakesonArray
