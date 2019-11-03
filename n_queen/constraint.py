#!/usr/bin/python
import sys
from z3 import *



def solve_n_queens(n) :
    ## message out
    print "solving %d queens problem" % n

    ## create symbols
    symbols = [Int("q_%d" % i) for i in range(n)]

    bounds_c = [ And(0 <= symbols[i], symbols[i] < n ) for i in range(n) ]

    rows_c = [ Distinct(symbols) ]

    slope_c = [ symbols[i] - symbols[j] != i - j for i in range(n-1) for j in range(i+1, n) ]
    slope2_c= [ symbols[j] - symbols[i] != i - j for i in range(n-1) for j in range(i+1, n) ]

    # solve(bounds_c + rows_c  + slope_c)
    s = Solver()
    s.add(bounds_c + rows_c + slope_c + slope2_c)
    if s.check() == sat :
        m = s.model()
        result = [m.evaluate(symbols[i]) for i in range(n)]
        print result
        board = [["x" if result[c] == r else "o" for c in range(n)] for r in range(n) ]
        for row in board :
            print " ".join(row)
    else :
        print "UNSAT"

def main() :

    if len(sys.argv) >= 2 :
        queens = int(sys.argv[1])
    else :
        queens = 8

    solve_n_queens(queens)

if __name__ == '__main__' :
    main()
