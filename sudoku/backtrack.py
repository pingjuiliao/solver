#!/usr/bin/env python
import sys
import math
import boards


def box_index(r, c) :
    return (r // 3) * 3 + c // 3

def test_box_index() :
    N = 9
    for i in range(N) :
        s= ""
        for j in range(N) :
            s += str(box_index(i, j)) + " "
        print s

def fill_number(n, r, c) :
    global board, rows, cols, boxes
    digit_idx = n - 1
    rows[r][digit_idx] = 1
    cols[c][digit_idx] = 1
    boxes[box_index(r, c)][digit_idx] = 1
    board[r][c] = str(n)

def erase_number(r, c) :
    global board, rows, cols, boxes
    digit_idx = int(board[r][c]) - 1
    rows[r][digit_idx] = 0
    cols[c][digit_idx] = 0
    boxes[box_index(r, c)][digit_idx] = 0
    board[r][c] = "."

def could_place(d, r, c) :
    global rows, cols, boxes
    idx = d-1
    return not ( rows[r][idx] == 1 or cols[c][idx] == 1 or boxes[box_index(r,c)][idx] == 1 )


def backtrack(r, c) :
    global solved, board, rows, cols, boxes

    N = 9
    if board[r][c] == "." :
        for d in range(1, 10) :
            if could_place(d, r, c) :
                fill_number(d, r, c)
                if r == N-1 and c == N-1:
                    solved = True
                elif c == N-1:
                    if r == 6 and board[0][6] == '6' and board[0][7] == '5' :
                        boards.print_board(board)
                    backtrack(r+1, 0)
                else :
                    if r == 8 and board[5][3] == '1' and board[0][7] == '5' :
                        boards.print_board(board)
                    backtrack(r, c+1)

                if not solved :
                    erase_number(r, c)


    else :
        if r == N-1 and c == N-1:
            solved = True
            return
        elif c == N-1 :
            backtrack(r+1, 0)
        else :
            backtrack(r, c+1)


def solve_one() :
    global board, rows, cols, boxes, solved
    n, N = 3, 9
    rows  = [ [0]*N for _ in range(N) ]
    cols  = [ [0]*N for _ in range(N) ]
    boxes = [ [0]*N for _ in range(N) ]
    for i in range(N) :
        for j in range(N) :
            if board[i][j] != '.' :
                fill_number(int(board[i][j]), i, j)

    boards.print_board(board)
    solved = False
    backtrack(0 ,0)
    if solved :
        print "Solved !!!"
        boards.print_board(board)
    else :
        print "Unsatisfiable !!!"

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
