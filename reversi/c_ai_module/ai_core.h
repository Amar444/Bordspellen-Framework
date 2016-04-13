static const int SIZE = 8;

typedef struct{
    int row;
    int col;
    int val;
} move;

move start(int board[SIZE][SIZE], int player, int depth);
move get_best_move(int board[SIZE][SIZE], int player, int depth, int alpha, int beta);
void valid_moves(int board[SIZE][SIZE], int player, int moves[SIZE][SIZE]);
void do_moves(int board[SIZE][SIZE], int row, int col, int player);
void copy_board(int board[SIZE][SIZE], int board_to_copy[SIZE][SIZE]);
int calc_value(int board[SIZE][SIZE], int player);