import numpy as np
from itertools import product
from copy import deepcopy
import sys, time

def read_in(input):
    if input is None:
        # basic example taken from https://sandiway.arizona.edu/sudoku/examples.html
        board = np.array([[0,0,0,2,6,0,7,0,1],
                                [6,8,0,0,7,0,0,9,0],
                                [1,9,0,0,0,4,5,0,0],
                                [8,2,0,1,0,0,0,4,0],
                                [0,0,4,6,0,2,9,0,0],
                                [0,5,0,0,0,3,0,2,8],
                                [0,0,9,3,0,0,0,7,4],
                                [0,4,0,0,5,0,0,3,6],
                                [7,0,3,0,1,8,0,0,0]])

        # the solution to the above example
        # board = np.array([[4,3,5,2,6,9,7,8,1],
        #                          [6,9,2,5,7,1,4,9,3],
        #                          [1,9,7,8,3,4,5,6,2],
        #                          [8,2,6,1,9,5,3,4,7],
        #                          [3,7,4,6,8,2,9,1,5],
        #                          [9,5,1,7,4,3,6,2,8],
        #                          [5,1,9,3,2,6,8,7,4],
        #                          [2,4,8,9,5,7,1,3,6],
        #                          [7,6,3,4,1,8,2,5,9]])

        # unsolvable example
        # board = np.array([[5,1,6,8,4,9,7,3,2],
        #                   [3,0,7,6,0,5,0,0,0],
        #                   [8,0,9,7,0,0,0,6,5],
        #                   [1,3,5,0,6,0,9,0,7],
        #                   [4,7,2,5,9,1,0,0,6],
        #                   [9,6,8,3,7,0,0,5,0],
        #                   [2,5,3,1,8,6,0,7,4],
        #                   [6,8,4,2,0,7,5,0,0],
        #                   [7,9,1,0,5,0,6,0,8]])

    else:
        # TODO check that input is clean
        board = np.loadtxt(input)

    return board

def check_if_complete(board):
    if check_if_valid(board) is True:
        if np.any(board == 0):
            return False
        else:
            return True

def check_if_valid(board):
    #row check
    for row_ind in range(board.shape[0]):
        to_check = board[row_ind, :]
        to_check = to_check[to_check > 0]
        if to_check.size != np.unique(to_check).size:
            return False

    #column check
    for col_ind in range(board.shape[1]):
        to_check = board[:, col_ind]
        to_check = to_check[to_check > 0]
        if to_check.size != np.unique(to_check).size:
            return False

    # box check
    for box_row_ind in range(3):
        for box_col_ind in range(3):
            box_u_l_inds = np.array([box_row_ind * 3, box_col_ind * 3])

            to_check = board[box_u_l_inds[0]:box_u_l_inds[0]+3, box_u_l_inds[1]:box_u_l_inds[1]+3].flatten()
            to_check = to_check[to_check > 0]
            if to_check.size != np.unique(to_check).size:
                return False

    return True

def check_if_guess_valid(board, guess, row, col):
    new_board = deepcopy(board)
    new_board[row, col] = guess

    #row check
    for row_ind in range(new_board.shape[0]):
        to_check = new_board[row_ind, :]
        to_check = to_check[to_check > 0]
        if to_check.size != np.unique(to_check).size:
            return False

    #column check
    for col_ind in range(new_board.shape[1]):
        to_check = new_board[:, col_ind]
        to_check = to_check[to_check > 0]
        if to_check.size != np.unique(to_check).size:
            return False

    # box check
    for box_row_ind in range(3):
        for box_col_ind in range(3):
            box_u_l_inds = np.array([box_row_ind * 3, box_col_ind * 3])

            to_check = new_board[box_u_l_inds[0]:box_u_l_inds[0]+3, box_u_l_inds[1]:box_u_l_inds[1]+3].flatten()
            to_check = to_check[to_check > 0]
            if to_check.size != np.unique(to_check).size:
                return False

    return True

def find_next_empty(board):
    for ix, iy in np.ndindex(board.shape):
        if board[iy, ix] == 0:
            return iy, ix
    return None, None

def solve(board):
    if check_if_complete(board) is True:
        print('Done')
        return True

    iy, ix = find_next_empty(board)
    if ix is None:
        print('Unsolveable')
        return False

    for guess in range(1, 10):
        if check_if_guess_valid(board, guess, iy, ix):
            board[iy, ix] = guess
            for _ in range(9):
                sys.stdout.write("\033[F") #back to previous line
                sys.stdout.write("\033[K") #clear line
            print(board)
            time.sleep(0.1)
            if solve(board) is True:
                return True

            board[iy, ix] = 0
    return False

if __name__ == '__main__':
    board = read_in(None)
    print(board)
    if solve(board) is False:
        print('unsolvable')
