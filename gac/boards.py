"""
Provides a variety of prebuilt board classes that can be used by games built upon
the library. Classes can be extended or used as mixins and all inherit from the
base Board class.
"""

from exceptions import *

class Board(object):
    """
    Represents an empty board
    """

    state = []

class TwoDimensionalBoard(Board):
    """
    Represents a 2-dimensional board
    """

    size = (0, 0)

    def __init__(self, x_size: int, y_size: int):
        """ Initializes a new, clear 2D board using the given X and Y sizes """
        self.resize(x_size, y_size)

    def check_coordinates(self, x: int, y: int):
        """ Checks whether the given coordinates are valid and within range of the current board """
        if not (0 <= x < self.size[0] or 0 <= y < self.size[1]):
            raise InvalidCoordinatesException("The given coordinates ({}, {}) are invalid for this board.".format(x, y))

    def resize(self, x_size: int, y_size: int):
        """ Applies a new size to the board """
        if x_size < 1 or y_size < 1:
            raise ValueError("A board must have at least 1 x and 1 y position.")

        self.size = (x_size, y_size)
        self.clear()

    def clear(self):
        """ Clears the board"""
        self.state = [[None for r in range(0, self.size[0])] for r in range(0, self.size[1])]

    def is_available(self, x: int, y: int):
        """ Returns whether a given spot on the board is available """
        self.check_coordinates(x, y)
        return self.state[x][y] is None

    def set(self, x: int, y: int, value: any):
        """ Saves a given value to the board on the given X and Y positions """
        if not (0 <= x < self.size[0] or 0 <= y < self.size[1]):
            raise InvalidCoordinatesException("The given coordinates ({}, {}) are invalid for this board.".format(x, y))

        self.state[x][y] = value

    def get(self, x: int, y: int):
        """ Returns the saved value from the board on the given X and Y positions """
        self.check_coordinates(x, y)
        return self.state[x][y]
