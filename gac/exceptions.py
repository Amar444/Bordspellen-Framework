"""
This file contains all exceptions that may be thrown by the GAC framework
"""

class InvalidCoordinatesException(Exception):
    """ Indicates invalid coordinates """

    coordinates = ()

    def __init__(self, x: int, y: int):
        """ Initializes a new InvalidCoordinatesException with the given coordinates """
        super().__init__("The given coordinates ({}, {}) are invalid for this board.".format(x, y))
        self.coordinates = (x, y)

    def get_coordinates(self):
        """ Returns the faulty coordinates that caused this Exception to occur """
        return self.coordinates
