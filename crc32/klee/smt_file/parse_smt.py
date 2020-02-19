#!/usr/bin/python
import sys
import z3

if len(sys.argv) < 2 :
    print("Usage: {} <smt2 file>".format(sys.argv[0]))
    quit()

s   = z3.Solver()
f   = z3.parse_smt2_file(sys.argv[1])
print(f)
