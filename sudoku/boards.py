import math
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

def hard_board() :
    hell1 = [[".",".","1","8","3",".",".",".","."],\
             ["9","6","5",".",".",".",".",".","."],\
             [".",".",".",".","1",".","9",".","."],\
             ["4",".",".",".",".",".",".","1","."],\
             [".",".","9","6",".","4","3",".","."],\
             [".","8",".",".",".",".",".",".","2"],\
             [".",".","7",".","9",".",".",".","."],\
             [".",".",".",".",".",".","5","4","8"],\
             [".",".",".",".","2","5","1",".","."]]
    return hell1

def really_hard_board() :
    hell1 = [["8",".",".",".",".",".",".",".","."],\
             [".",".","3","6",".",".",".",".","."],\
             [".","7",".",".","9",".","2",".","."],\
             [".","5",".",".",".","7",".",".","."],\
             [".",".",".",".","4","5","7",".","."],\
             [".",".",".","1",".",".",".","3","."],\
             [".",".","1",".",".",".",".","6","8"],\
             [".",".","8","5",".",".",".","1","."],\
             [".","9",".",".",".",".","4",".","."],\
             ]
    return hell1
