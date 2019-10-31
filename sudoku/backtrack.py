#!/usr/bin/env python
import sys
import math
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

def print_board(b) :
    print "-" * 24
    N = len(b)
    n = int(math.sqrt(N))
    for i in range(N) :
        if i % n == 0 :
            print "-" * 22
        s = ""
        for j in range(N) :
            if j % n == 0 :
                s += "| "
            s += str(b[i][j])
        print s + " |"
    print "-" * 24

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
    return not ( rows[r][idx] == 1 or cols[c][idx] == 1 or  boxes[box_index(r,c)][idx] == 1 )


def backtrack(r, c) :
    global solved, board, rows, cols, boxes

    N = 9
    if board[r][c] == "." :
        for d in range(1, 10) :
            if could_place(d, r, c) :
                fill_number(d, r, c)
                if r == N-1 and c == N-1:
                    solved == True
                elif c == N-1:
                    backtrack(r+1, 0)
                else :
                    backtrack(r, c+1)

                if not solved :
                    erase_number(r, c)


    else :
        if r == N-1 and c == N-1:
            solved = True
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

    print_board(board)
    # test_box_index()
    solved = False
    backtrack(0 ,0)
    if solved :
        print "Solved !!!"
        print_board(board)
    else :
        print "Unsatisfiable !!!"

def main() :
    global board
    board = test_board()
    solve_one()

if __name__ == '__main__' :
    main()
