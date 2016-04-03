"""
Unit Tests for the Reversi implementation
"""
from game import ReversiBoard, ReversiGame

_PLAYER_ONE = "w"
_PLAYER_TWO = "b"
player_one_win_board = None
player_two_win_board = None
initial_board = None
board_state_one = None
board_state_two = None


def board_init():
    """ init a 2D board with reversi board sizes"""
    return ReversiBoard()


def init_test_boards():
    """ Creates a few game boards with different states for testing. See boards.txt for a visual version"""

    global initial_board
    global player_one_win_board
    global player_two_win_board
    global board_state_one
    global board_state_two

    initial_board = board_init()
    player_one_win_board = board_init()
    player_two_win_board = board_init()
    board_state_one = board_init()
    board_state_two = board_init()

    # creating initial board Score = 2 for both players, both players have 4 possible moves
    initial_board.set(3, 3, _PLAYER_ONE)
    initial_board.set(4, 4, _PLAYER_ONE)
    initial_board.set(3, 4, _PLAYER_TWO)
    initial_board.set(4, 3, _PLAYER_TWO)

    # setting a player one win board P1 score = 17, P2 score = 12
    player_one_win_board.set(0, 0, _PLAYER_ONE)
    player_one_win_board.set(0, 1, _PLAYER_ONE)
    player_one_win_board.set(0, 2, _PLAYER_ONE)
    player_one_win_board.set(0, 3, _PLAYER_ONE)
    player_one_win_board.set(0, 4, _PLAYER_ONE)
    player_one_win_board.set(0, 5, _PLAYER_ONE)
    player_one_win_board.set(0, 6, _PLAYER_ONE)
    player_one_win_board.set(0, 7, _PLAYER_ONE)
    player_one_win_board.set(1, 0, _PLAYER_ONE)
    player_one_win_board.set(1, 1, _PLAYER_ONE)
    player_one_win_board.set(1, 2, _PLAYER_ONE)
    player_one_win_board.set(1, 3, _PLAYER_ONE)
    player_one_win_board.set(1, 4, _PLAYER_ONE)
    player_one_win_board.set(2, 0, _PLAYER_ONE)
    player_one_win_board.set(2, 1, _PLAYER_ONE)
    player_one_win_board.set(2, 2, _PLAYER_ONE)
    player_one_win_board.set(2, 3, _PLAYER_ONE)
    player_one_win_board.set(4, 1, _PLAYER_TWO)
    player_one_win_board.set(4, 2, _PLAYER_TWO)
    player_one_win_board.set(4, 3, _PLAYER_TWO)
    player_one_win_board.set(5, 2, _PLAYER_TWO)
    player_one_win_board.set(5, 3, _PLAYER_TWO)
    player_one_win_board.set(6, 2, _PLAYER_TWO)
    player_one_win_board.set(6, 3, _PLAYER_TWO)
    player_one_win_board.set(7, 2, _PLAYER_TWO)
    player_one_win_board.set(7, 3, _PLAYER_TWO)
    player_one_win_board.set(7, 6, _PLAYER_TWO)
    player_one_win_board.set(6, 5, _PLAYER_TWO)
    player_one_win_board.set(5, 4, _PLAYER_TWO)

    # setting a player two win board Player one score = 3, Player 2 score = 19, possible moves = 2x0
    player_two_win_board.set(3, 5, _PLAYER_ONE)
    player_two_win_board.set(3, 6, _PLAYER_ONE)
    player_two_win_board.set(3, 7, _PLAYER_ONE)
    player_two_win_board.set(3, 0, _PLAYER_TWO)
    player_two_win_board.set(3, 1, _PLAYER_TWO)
    player_two_win_board.set(3, 2, _PLAYER_TWO)
    player_two_win_board.set(3, 3, _PLAYER_TWO)
    player_two_win_board.set(3, 4, _PLAYER_TWO)
    player_two_win_board.set(4, 2, _PLAYER_TWO)
    player_two_win_board.set(4, 3, _PLAYER_TWO)
    player_two_win_board.set(5, 0, _PLAYER_TWO)
    player_two_win_board.set(6, 0, _PLAYER_TWO)
    player_two_win_board.set(7, 0, _PLAYER_TWO)
    player_two_win_board.set(5, 1, _PLAYER_TWO)
    player_two_win_board.set(6, 1, _PLAYER_TWO)
    player_two_win_board.set(7, 1, _PLAYER_TWO)
    player_two_win_board.set(5, 2, _PLAYER_TWO)
    player_two_win_board.set(6, 2, _PLAYER_TWO)
    player_two_win_board.set(7, 2, _PLAYER_TWO)
    player_two_win_board.set(5, 3, _PLAYER_TWO)
    player_two_win_board.set(6, 3, _PLAYER_TWO)
    player_two_win_board.set(7, 3, _PLAYER_TWO)

    # setting up a midgame board: Part 1. P1 score = 5, P2 score = 5, Possible moves P1 = 5, P2 = 7
    board_state_one.set(1, 1, _PLAYER_TWO)
    board_state_one.set(2, 2, _PLAYER_TWO)
    board_state_one.set(3, 3, _PLAYER_TWO)
    board_state_one.set(4, 4, _PLAYER_TWO)
    board_state_one.set(5, 5, _PLAYER_TWO)
    board_state_one.set(2, 3, _PLAYER_ONE)
    board_state_one.set(2, 4, _PLAYER_ONE)
    board_state_one.set(3, 4, _PLAYER_ONE)
    board_state_one.set(4, 3, _PLAYER_ONE)
    board_state_one.set(5, 2, _PLAYER_ONE)

    # setting up a midgame board. Part 2. P1 score = 9, P2 score = 6, Possible moves P1 =12, P2= 13
    board_state_two.set(0, 1, _PLAYER_TWO)
    board_state_two.set(1, 2, _PLAYER_TWO)
    board_state_two.set(1, 3, _PLAYER_TWO)
    board_state_two.set(3, 4, _PLAYER_TWO)
    board_state_two.set(4, 2, _PLAYER_TWO)
    board_state_two.set(4, 4, _PLAYER_TWO)
    board_state_two.set(1, 4, _PLAYER_ONE)
    board_state_two.set(2, 2, _PLAYER_ONE)
    board_state_two.set(2, 3, _PLAYER_ONE)
    board_state_two.set(2, 4, _PLAYER_ONE)
    board_state_two.set(3, 2, _PLAYER_ONE)
    board_state_two.set(3, 3, _PLAYER_ONE)
    board_state_two.set(3, 5, _PLAYER_ONE)
    board_state_two.set(4, 3, _PLAYER_ONE)
    board_state_two.set(5, 3, _PLAYER_ONE)


def test_legal_moves():
    """ tests the get_legal_moves function, implcitly tests is_legal_move"""
    test_game = ReversiGame()
    test_game.board = initial_board
    print("Testing initial_board")
    print(len(test_game.get_legal_moves(_PLAYER_ONE)) == 4)
    print(len(test_game.get_legal_moves(_PLAYER_TWO)) == 4)

    test_game.board = player_one_win_board
    print("Testing p1win")
    print(len(test_game.get_legal_moves(_PLAYER_ONE)) == 0)
    print(len(test_game.get_legal_moves(_PLAYER_TWO)) == 0)

    test_game.board = player_two_win_board
    print("Testing p2win")
    print(len(test_game.get_legal_moves(_PLAYER_ONE)) == 0)
    print(len(test_game.get_legal_moves(_PLAYER_TWO)) == 0)

    test_game.board = board_state_one
    print("Testing board state 1")
    print(len(test_game.get_legal_moves(_PLAYER_ONE)) == 5)
    print(len(test_game.get_legal_moves(_PLAYER_TWO)) == 7)

    test_game.board = board_state_two
    print("Testing board state 2")
    print(len(test_game.get_legal_moves(_PLAYER_ONE)) == 12)
    print(len(test_game.get_legal_moves(_PLAYER_TWO)) == 11)


def test_execute_move():
    """ Test the execute move method"""
    print("\nTesting stone placements")
    test_game = ReversiGame()
    test_game.board = initial_board
    try:
        test_game.execute_move(_PLAYER_ONE, 2, 4)
        if test_game.board.get(2, 4) == _PLAYER_ONE:
            print("True")
        else:
            print("False: stone didn't change")
    except:
        print("This shouldn't be thrown")
    try:
        test_game.execute_move(_PLAYER_ONE, 0, 0)
        print("False")
    except:
        print("Exception succesfully thrown")

    test_game.board = board_state_two
    try:
        test_game.execute_move(_PLAYER_ONE, 5, 4)
        if test_game.board.get(5, 4) == _PLAYER_ONE and test_game.board.get(4, 4) == _PLAYER_ONE:
            print("True")
        else:
            print("Error: Stone didn't change")
    except:
        print("This Shouldn't Be Thrown")


if __name__ == '__main__':
    print("Testing Reversi Methods")
    init_test_boards()
    test_legal_moves()
    test_execute_move()
