"""
Unit Tests for the Reversi implementation
"""
import unittest
from game import ReversiBoard, ReversiGame

_PLAYER_ONE = "w"
_PLAYER_TWO = "b"

def create_initial_board():
    """ Creating initial board Score = 2 for both players, both players have 4 possible moves """
    board = ReversiBoard()
    board.set(3, 3, _PLAYER_ONE)
    board.set(4, 4, _PLAYER_ONE)
    board.set(3, 4, _PLAYER_TWO)
    board.set(4, 3, _PLAYER_TWO)
    return board

def create_player_one_win_board():
    """ setting a player one win board P1 score = 17, P2 score = 12 """
    board = ReversiBoard()
    board.set(0, 0, _PLAYER_ONE)
    board.set(0, 1, _PLAYER_ONE)
    board.set(0, 2, _PLAYER_ONE)
    board.set(0, 3, _PLAYER_ONE)
    board.set(0, 4, _PLAYER_ONE)
    board.set(0, 5, _PLAYER_ONE)
    board.set(0, 6, _PLAYER_ONE)
    board.set(0, 7, _PLAYER_ONE)
    board.set(1, 0, _PLAYER_ONE)
    board.set(1, 1, _PLAYER_ONE)
    board.set(1, 2, _PLAYER_ONE)
    board.set(1, 3, _PLAYER_ONE)
    board.set(1, 4, _PLAYER_ONE)
    board.set(2, 0, _PLAYER_ONE)
    board.set(2, 1, _PLAYER_ONE)
    board.set(2, 2, _PLAYER_ONE)
    board.set(2, 3, _PLAYER_ONE)
    board.set(4, 1, _PLAYER_TWO)
    board.set(4, 2, _PLAYER_TWO)
    board.set(4, 3, _PLAYER_TWO)
    board.set(5, 2, _PLAYER_TWO)
    board.set(5, 3, _PLAYER_TWO)
    board.set(6, 2, _PLAYER_TWO)
    board.set(6, 3, _PLAYER_TWO)
    board.set(7, 2, _PLAYER_TWO)
    board.set(7, 3, _PLAYER_TWO)
    board.set(7, 6, _PLAYER_TWO)
    board.set(6, 5, _PLAYER_TWO)
    board.set(5, 4, _PLAYER_TWO)
    return board

def create_player_two_win_board():
    """ setting a player two win board Player one score = 3, Player 2 score = 19, possible moves = 2x0 """
    board = ReversiBoard()
    board.set(3, 5, _PLAYER_ONE)
    board.set(3, 6, _PLAYER_ONE)
    board.set(3, 7, _PLAYER_ONE)
    board.set(3, 0, _PLAYER_TWO)
    board.set(3, 1, _PLAYER_TWO)
    board.set(3, 2, _PLAYER_TWO)
    board.set(3, 3, _PLAYER_TWO)
    board.set(3, 4, _PLAYER_TWO)
    board.set(4, 2, _PLAYER_TWO)
    board.set(4, 3, _PLAYER_TWO)
    board.set(5, 0, _PLAYER_TWO)
    board.set(6, 0, _PLAYER_TWO)
    board.set(7, 0, _PLAYER_TWO)
    board.set(5, 1, _PLAYER_TWO)
    board.set(6, 1, _PLAYER_TWO)
    board.set(7, 1, _PLAYER_TWO)
    board.set(5, 2, _PLAYER_TWO)
    board.set(6, 2, _PLAYER_TWO)
    board.set(7, 2, _PLAYER_TWO)
    board.set(5, 3, _PLAYER_TWO)
    board.set(6, 3, _PLAYER_TWO)
    board.set(7, 3, _PLAYER_TWO)
    return board

def create_board_state_one():
    """ Setting up a midgame board: Part 1. P1 score = 5, P2 score = 5, Possible moves P1 = 5, P2 = 7 """
    board = ReversiBoard()
    board.set(1, 1, _PLAYER_TWO)
    board.set(2, 2, _PLAYER_TWO)
    board.set(3, 3, _PLAYER_TWO)
    board.set(4, 4, _PLAYER_TWO)
    board.set(5, 5, _PLAYER_TWO)
    board.set(2, 3, _PLAYER_ONE)
    board.set(2, 4, _PLAYER_ONE)
    board.set(3, 4, _PLAYER_ONE)
    board.set(4, 3, _PLAYER_ONE)
    board.set(5, 2, _PLAYER_ONE)
    return board

def create_board_state_two():
    """ Setting up a midgame board. Part 2. P1 score = 9, P2 score = 6, Possible moves P1 =12, P2= 13 """
    board = ReversiBoard()
    board.set(0, 1, _PLAYER_TWO)
    board.set(1, 2, _PLAYER_TWO)
    board.set(1, 3, _PLAYER_TWO)
    board.set(3, 4, _PLAYER_TWO)
    board.set(4, 2, _PLAYER_TWO)
    board.set(4, 4, _PLAYER_TWO)
    board.set(1, 4, _PLAYER_ONE)
    board.set(2, 2, _PLAYER_ONE)
    board.set(2, 3, _PLAYER_ONE)
    board.set(2, 4, _PLAYER_ONE)
    board.set(3, 2, _PLAYER_ONE)
    board.set(3, 3, _PLAYER_ONE)
    board.set(3, 5, _PLAYER_ONE)
    board.set(4, 3, _PLAYER_ONE)
    board.set(5, 3, _PLAYER_ONE)
    return board


class TestLegalMoves(unittest.TestCase):
    """ Tests the get_legal_moves function, implicitly tests is_legal_move"""
    def test_legal_moves(self):
        test_game = ReversiGame()
        test_game.board = create_initial_board()

        print("\nTesting legal moves")
        print("Testing initial_board")
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_ONE)), 4)
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_TWO)), 4)

        test_game.board = create_player_one_win_board()
        print("Testing p1win")
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_ONE)), 0)
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_TWO)), 0)

        test_game.board = create_player_two_win_board()
        print("Testing p2win")
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_ONE)), 0)
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_TWO)), 0)

        test_game.board = create_board_state_one()
        print("Testing board state 1")
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_ONE)), 5)
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_TWO)), 7)

        test_game.board = create_board_state_two()
        print("Testing board state 2")
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_ONE)), 12)
        self.assertEqual(len(test_game.get_legal_moves(_PLAYER_TWO)), 11)


class TestExecuteMove(unittest.TestCase):
    """ Test the execute move method"""
    def test_execute_move(self):
        test_game = ReversiGame()

        print("\nTesting stone placements")
        test_game.board = create_initial_board()
        test_game.execute_move(_PLAYER_ONE, 2, 4)
        self.assertEqual(test_game.board.get(2, 4), _PLAYER_ONE)

        with self.assertRaises(ValueError):
            test_game.execute_move(_PLAYER_ONE, 0, 0)

        test_game.board = create_board_state_two()
        test_game.execute_move(_PLAYER_ONE, 5, 4)

        self.assertEqual(test_game.board.get(5, 4) == _PLAYER_ONE and test_game.board.get(4, 4) == _PLAYER_ONE, True)


class TestScores(unittest.TestCase):
    def test_scores(self):
        test_game = ReversiGame()

        print("\nTesting get_score")
        test_game.board = create_initial_board()
        self.assertEqual(test_game.get_score(_PLAYER_ONE), 2)
        self.assertEqual(test_game.get_score(_PLAYER_TWO), 2)

        test_game.board = create_player_one_win_board()
        self.assertEqual(test_game.get_score(_PLAYER_ONE), 17)
        self.assertEqual(test_game.get_score(_PLAYER_TWO), 12)

        test_game.board = create_player_two_win_board()
        self.assertEqual(test_game.get_score(_PLAYER_ONE), 3)
        self.assertEqual(test_game.get_score(_PLAYER_TWO), 19)

        test_game.board = create_board_state_one()
        self.assertEqual(test_game.get_score(_PLAYER_ONE), 5)
        self.assertEqual(test_game.get_score(_PLAYER_TWO), 5)

        test_game.board = create_board_state_two()
        self.assertEqual(test_game.get_score(_PLAYER_ONE), 9)
        self.assertEqual(test_game.get_score(_PLAYER_TWO), 6)


class TestGameValue(unittest.TestCase):
    def test_game_value(self):
        test_game = ReversiGame()

        print("\nTesting Game Values")
        test_game.board = create_initial_board()
        self.assertEqual(test_game.get_value(_PLAYER_ONE, _PLAYER_TWO), 2)

        test_game.board = create_player_one_win_board()
        self.assertEqual(test_game.get_value(_PLAYER_ONE, _PLAYER_TWO), 3)

        test_game.board = create_player_two_win_board()
        self.assertEqual(test_game.get_value(_PLAYER_ONE, _PLAYER_TWO), 0)

        test_game.board = create_board_state_one()
        self.assertEqual(test_game.get_value(_PLAYER_ONE, _PLAYER_TWO), 2)

        test_game.board = create_board_state_two()
        self.assertEqual(test_game.get_value(_PLAYER_ONE, _PLAYER_TWO), 2)

if __name__ == '__main__':
    unittest.main()
