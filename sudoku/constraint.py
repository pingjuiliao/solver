#!/usr/bin/env python
import sys
import math
import boards
from z3 import *
def test_board() :
    test1 = [["5","3",".",".","7",".",".",".","."],\
             ["6",".",".","1","9","5",".",".","."],\
             [".","9","8",".",".",".",".","6","."],\
             ["8",".",".",".","6",".",".",".","3"],\
             ["4",".",".","8",".","3",".",".","1"],\
             ["7",".",".",".","2",".",".",".","6"],\
             [".","6",".",".",".",".","2","8","."],\
             [".",".",".","4","1","9",".",".","5"],\
             [".",".",".",".","8",".",".","7","9"]]

    return test1

def box_index(r, c) :
    return (r // 3) * 3 + c // 3

def test_box_index() :
    N = 9
    for i in range(N) :
        s= ""
        for j in range(N) :
            s += str(box_index(i, j)) + " "
        print s

def solve_one() :
    global board
    boards.print_board(board)
    # 9x9 matrix of integer variables
    X = [ [ Int("x_%s_%s" % (i+1, j+1)) for j in range(9)  ]
                  for i in range(9) ]

    # each cell contains a value in {1, ..., 9}
    cells_c  = [ And(1 <= X[i][j], X[i][j] <= 9)
                         for i in range(9) for j in range(9) ]

    # each row contains a digit at most once
    rows_c   = [ Distinct(X[i]) for i in range(9)  ]

    # each column contains a digit at most once
    cols_c   = [ Distinct([ X[i][j] for i in range(9)  ])
                         for j in range(9) ]

    # each 3x3 square contains a digit at most once
    sq_c     = [ Distinct([ X[3*i0 + i][3*j0 + j]
                                for i in range(3) for j in range(3) ])
                                             for i0 in range(3) for j0 in range(3) ]

    sudoku_c = cells_c + rows_c + cols_c + sq_c
    board_c  = [ If(board[i][j] == '.', True, X[i][j] == (ord(board[i][j]) - 0x30) ) for i in range(9) for j in range(9) ]

    s = Solver()
    s.add(sudoku_c + board_c)
    if s.check() == sat :
        m= s.model()
        # r = [ [m.evaluate(X[i][j]) for j in range(9)] for i in range(9) ]
        #print_matrix(r)
        for i in range(9) :
            for j in range(9) :
                board[i][j] = m.evaluate(X[i][j])
        boards.print_board(board)
    else :
        print "failed to solve"

def main() :
    global board
    board = boards.test_board()
    solve_one()
    board = boards.hard_board()
    solve_one()
    board = boards.really_hard_board()
    solve_one()

if __name__ == '__main__' :
    main()
