"""
This file contains all exceptions that may be thrown by the GAC framework
"""

class InvalidCoordinatesException(Exception):
    """ Indicates invalid coordinates """
    pass

class InvalidBoardException(Exception):
    """ Invalid board exception """
    pass

class InvalidCommandException(Exception):
    """ Invalid command exception """
    pass