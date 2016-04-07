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

    last_turn = None
    state = []

class TwoDimensionalBoard(Board):
    """
    Represents a 2-dimensional board
    """

    size = (0, 0)

    def __init__(self, x_size: int=0, y_size: int=0, *args, **kwargs):
        """ Initializes a new, clear 2D board using the given X and Y sizes """
        super().__init__(*args, **kwargs)
        if self.size != (0, 0) and (x_size, y_size) == (0, 0):
            self.resize(self.size[0], self.size[1])
        else:
            self.resize(x_size, y_size)

    def check_coordinates(self, x: int, y: int):
        """ Checks whether the given coordinates are valid and within range of the current board """
        if not (0 <= x < self.size[0] or 0 <= y < self.size[1]):
            raise InvalidCoordinatesException(x, y)

    def resize(self, x_size: int, y_size: int):
        """ Applies a new size to the board """
        if x_size < 1 or y_size < 1:
            raise ValueError("A board must have at least 1 x and 1 y position.")

        self.size = (x_size, y_size)
        self.clear()

    def clear(self):
        """ Clears the board"""
        self.state = [[None for r in range(0, self.size[0])] for r in range(0, self.size[1])]

    def is_available(self, x: int, y: int, check: bool=True):
        """ Returns whether a given spot on the board is available """
        if check:
            self.check_coordinates(x, y)
        return self.state[x][y] is None

    def set(self, x: int, y: int, value: any, check: bool=True):
        """ Saves a given value to the board on the given X and Y positions """
        if check:
            self.check_coordinates(x, y)
        self.state[x][y] = value
        self.last_turn = (x, y, value)

    def get(self, x: int, y: int, check: bool=True):
        """ Returns the saved value from the board on the given X and Y positions """
        if check:
            self.check_coordinates(x, y)
        return self.state[x][y]

    def is_full(self):
        """
        Check whether the board is full. The method is doing this with checking the entries in the two arrays from
        the board and will directly return it's result when it finds out if there is still place for another move
        """
        return not any(None in b for b in self.state)

    def __str__(self):
        """ Returns the current board as a string """
        return "\n".join(["".join([(lambda y: str(y) if y else None)(y) or '-' for y in x]) for x in self.state])
