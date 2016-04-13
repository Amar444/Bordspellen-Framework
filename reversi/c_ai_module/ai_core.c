#include "ai_core.h"
#include <sys/time.h>
#define NULL '\0' /*defines NULL as NULL pointer */

const int DIRECTIONS[8][2] = {{-1,-1},{-1,0},{-1,1},{0,-1},{0,1},{1,-1},{1,0},{1,1}};
const int DIRECTIONS_LENGTH = 8;
const int WEIGHTS[8][8] = {{120, -20, 20,  5,  5, 20,-20,120},
                          {-20, -40, -5, -5, -5, -5,-40,-20},
                          {20,  -5,  15,  3,  3, 15, -5, 20},
                          {5,   -5,   3,  3,  3,  3, -5,  5},
                          {5,   -5,   3,  3,  3,  3, -5,  5},
                          {20,  -5,  15,  3,  3, 15, -5, 20},
                          {-20,-40,  -5, -5, -5, -5,-40,-20},
                          {120,-20,  20,  5,  5, 20,-20,120}};
int ai_player;
int analyzed_moves = 0;
struct timeval starttime, endtime;

/*init for the ai, called from the wrapper*/
move start(int board[SIZE][SIZE], int player, int depth){
    gettimeofday(&starttime, NULL);
    /*printf("\n%ld\n", starttime);*/
    ai_player = player;
    analyzed_moves = 0;
    int alpha = -2147483647;
    int beta = 2147483647;
    move ret = get_best_move(board, player, depth, alpha, beta);
    printf("Analyzed %i moves.\n", analyzed_moves);
    return ret;
}

/*the basic minimax structure*/
move get_best_move(int board[SIZE][SIZE], int player, int depth, int alpha, int beta){
    move end = {10,10,calc_value(board, player)};
    gettimeofday(&endtime, NULL);
    if(depth == 0 || (((endtime.tv_sec - starttime.tv_sec) >= 3) && ((endtime.tv_usec - starttime.tv_usec) > 700000))){
        /*if(depth > 0){
            printf("time diference: %i.%lu\n", endtime.tv_sec - starttime.tv_sec, endtime.tv_usec - starttime.tv_usec );
        }*/
        return end;
    }

    /*initialize an array of 0's to store legit moves*/
    int moves[SIZE][SIZE];
    int output_board[SIZE][SIZE];
    int i,j;
    move result;
    move best_result = player == ai_player ? (move){0,0,calc_value(board, player) } : (move){0,0,calc_value(board, player)};

    /* set the opponent*/
    int opp = (player == 1 ? 2 : 1);
    /*initialize moves array*/
    for(i=0;i<SIZE;i++){
        for(j=0;j<SIZE;j++){
            moves[i][j] = 0;
        }
    }
    valid_moves(board, player, moves); /*fill the moves array*/
    if(moves[0][0] == 4){
        return end;
    }

    for(i=0;i<SIZE;i++){
        for(j=0;j<SIZE;j++){
            if(moves[i][j]){
                copy_board(output_board, board);
                do_moves(output_board, i, j, player);
                result = get_best_move(output_board, opp, depth-1, alpha, beta);
                analyzed_moves++;

                if(player == ai_player){

                    if(result.val > alpha){
                        alpha = result.val;
                        best_result.row = i;
                        best_result.col = j;
                        best_result.val = alpha;
                        if(beta <= alpha){
                            move ret = {i, j, alpha};
                            /*printf("row = %i, col =%i \n", ret.row, ret.col);*/
                            return ret;
                        }
                    }
                }
                else{
                    if(result.val < beta){
                        beta = result.val;
                        best_result.row = i;
                        best_result.col = j;
                        best_result.val = beta;
                        if(beta <= alpha){
                            move ret = {i, j, beta};
                            /*printf("row = %i, col =%i \n", ret.row, ret.col);*/
                            return ret;
                        }
                    }
                }
            }
        }
    }

    /*printf("The output_board array.\n");
    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            printf("%i ", output_board[i][j]);
        }
        printf("\n");
    }
    printf("REACHED THE END OF SERIES WITH %i, %i, %i\n", best_result.row, best_result.col, best_result.val);
    */
    return best_result;

}

/*returns valid moves for a player*/
void valid_moves(int board[SIZE][SIZE], int player, int moves[SIZE][SIZE]){
    int row = 0;
    int col = 0;
    int row_to_check = 0;
    int col_to_check = 0;
    /*int opp = (player == 1) ? 2 : 1; DEPRECATED */
    int direction; /*direction counter for loops*/
    int length; /*length counter for checking moves*/
    int spotted_opponent = 0; /*C doesn't have booleans, 0 = false and non-zero = true though*/
    int token = 0; /*token used to store a player or empty*/
    int move_counter = 0; /*Used to determine how many moves there are*/

    for(row = 0; row<SIZE; row++){
        for(col = 0; col<SIZE; col++){
            if(board[row][col] != 0){
            /* continue if the square isn't empty*/
                continue;
            }
            /*loop over directions and check if this move became valid already*/
            for(direction = 0; direction < DIRECTIONS_LENGTH && moves[row][col] == 0; direction++){
                spotted_opponent = 0;
                for(length = 1; length < SIZE; length++){
                    row_to_check = row + DIRECTIONS[direction][0] * length;
                    col_to_check = col + DIRECTIONS[direction][1] * length;
                    if(row_to_check < 0 || row_to_check >= SIZE || col_to_check < 0 || col_to_check >= SIZE){
                        /*break length loop if out of bounds*/
                        break;
                    }
                    token = board[row_to_check][col_to_check];
                    if(token == 0){
                        break;
                    }
                    if(token == player){
                        if(spotted_opponent){
                            moves[row][col] = 1;
                            move_counter++;
                            break;
                        }
                        break;
                    }
                    else{
                        spotted_opponent = 1;
                    }
                }
            }

        }
    }

    if(move_counter == 0){
        moves[0][0] = 4;
    }
}

void do_moves(int board[SIZE][SIZE], int row, int col, int player){
    /*THIS FUNCTION DOES NO CHECKING IF YOUR MOVE IS VALID IN ORDER TO SAVE TIME*/
    board[row][col] = player;
    int opp = (player == 1) ? 2 : 1;
    int direction, distance, row_to_change, col_to_change, token;
    for(direction = 0; direction < DIRECTIONS_LENGTH; direction++){
        for(distance = 1; distance<SIZE; distance++){
            row_to_change = row + DIRECTIONS[direction][0] * distance;
            col_to_change = col + DIRECTIONS[direction][1] * distance;
            if(row_to_change < 0 || row_to_change >= SIZE || col_to_change < 0 || col_to_change >= SIZE){
                        /*break length loop if out of bounds*/
                        break;
            }
            token = board[row_to_change][col_to_change];
            if(token == opp){
                board[row_to_change][col_to_change] = player;
                continue;
            }
            /*break if not an opponent*/
            break;
        }
    }
}

void copy_board(int board[SIZE][SIZE], int board_to_copy[SIZE][SIZE]){
    int i,j; /*for iteration*/
    for(i=0;i<SIZE;i++){
        for(j=0;j<SIZE;j++){
            board[i][j] = board_to_copy[i][j];
        }
    }
}

int calc_value(int board[SIZE][SIZE], int player){
    int i,j,ret = 0;
    int opp = player == ai_player ? 2 : 1;
    for(i=0;i<SIZE;i++){
        for(j=0;j<SIZE;j++){
            if(board[i][j] == player){
                ret += WEIGHTS[i][j];
            }
            if(board[i][j] == opp){
                ret -= WEIGHTS[i][j];
            }
        }
    }

    return ret;
}