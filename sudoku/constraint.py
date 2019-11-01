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


def solve_one() :
    """
    a11 a12 a13 | b14 b15 b16 | c17 c18 c19
    a21 a22 a23 | b24 b25 b26 | c27 c28 c29
    a31 a32 a33 | b34 b35 b36 | c37 c38 c39
    ---------------------------------------
    d41 d42 d43 | e44 e45 e46 | f47 f48 f49
    d51 d52 d53 | e54 e55 e66 | f57 f58 f59
    d61 d62 d63 | e64 e65 e66 | f67 f68 f69
    ---------------------------------------
    g71 g72 g73 | h74 h75 h76 | i77 i78 i79
    g81 g82 g83 | h84 h85 h86 | i87 i88 i89
    g91 g92 g93 | h94 h95 h96 | i97 i98 i99

    """
    a11 =

def main() :
    global board
    board = test_board()
    solve_one()

if __name__ == '__main__' :
    main()
