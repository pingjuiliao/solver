#!/usr/bin/python
from z3 import *

def stoi(_str) :
    length = 0
    L = len(_str)
    while length < L and _str[length] in "0123456789" :
        length += 1
    return int(_str[:length]), length

def evaluate(left, operator, right) :
    val = None
    ## print "evaluating ", left, operator, right
    if operator == "+" :
        val = left + right
    elif operator == "-" :
        val = left - right
    elif operator == "*" :
        val = left * right
    elif operator == "/" :
        val = left / right
    else :
        print "Wrong Operator %s" % operator
        quit()

    if val > 2147483647 or val < -2147483648 :
        print "Overflow !! %d" % val
        quit()
    return val

def solve_one(s) :
    global syms
    syms = [ Int("s_%s" % str(i)) for i in range(L) ]

    ## simulate the control flow of CROMU_00017
    i = is_neg = 0
    operStack = []
    numStack = []
    while i < L :

        curr = s[i]

        ## switch
        if curr == " " :
            i+= 1
            continue
        if curr in "0123456789" :
            if operStack and s[i] == '-' :
                operStack.pop('-')
                operStack.append('+')
                is_neg = 1

            val, moved = stoi(s[i:]) ## s[i:i+ moved] == "<numbers>"
            if is_neg :
                val *= -1
            is_neg = 0

            numStack.append(val)
            i += moved
            continue
        if curr == "(" :
            operStack.append(curr)
            i += 1
            continue
        if curr == ")" :
            ## most complex logic
            if not operStack :
                print s, "wrong equation"
                quit()
            op = operStack[-1]
            while op != '(' :
                rarg =  numStack.pop()
                larg =  numStack.pop()
                op   = operStack.pop()
                numStack.append(evaluate(larg, op, rarg))
                op   = operStack[-1]
            if op == '(' :
                operStack.pop()

            i += 1
            continue
        if curr == '+' or curr == '-' :
            prev_op = None if not operStack else operStack[-1]
            if prev_op and prev_op in "+-*/" :
                rarg = numStack.pop()
                larg = numStack.pop()
                prev_op = operStack.pop()
                numStack.append(evaluate(larg, prev_op, rarg))

            operStack.append(curr)
            i += 1
            continue
        if curr == '*' or curr == '/' :
            prev_op = None if not operStack else operStack[-1]
            if prev_op and prev_op in '*/' :
                rarg = numStack.pop()
                larg = numStack.pop()
                prev_op = operStack.pop()
                numStack.append(evaluate(larg, prev_op, rarg))

            operStack.append(curr)
            i += 1
            continue

    ## end of while
    b = None if not numStack else numStack.pop()
    while operStack :
        a  = numStack.pop()
        op = operStack.pop()
        #tmp  = eval(" ".join([str(a), op, str(b)]))
        tmp = evaluate(a, op, b)
        b = tmp

    return b

def get_equations() :
    global index
    with open("equations.txt", "rb") as f :
        eqs = f.read()
        f.close()
    return eqs.split('\n')

def main() :
    eqs = get_equations()
    for eq in eqs :
        if len(eq) == 0 :
            continue
        my_answer = solve_one(eq)
        answer    = eval(eq)
        print eq , " = ? "
        print "Your answer : ", my_answer, "\nThe  answer : ", answer
        if answer == my_answer :
            print "[O] **Correct**\n\n"
        else :
            print "[X] Incorrect\n\n"

if __name__ == '__main__' :
    main()
