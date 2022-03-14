from datetime import timedelta
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt
import itertools as tools
import utilities as u
from csv import writer

x,y,z = symbols(["x","y","z"])
_symbols = [x,y,z]
# shown symbols

S0, S1, S2, S3, S4, S5, S6, S7, S8, S9  = symbols(["S0","S1","S2","S3","S4","S5","S6","S7","S8","S9"])
_safeSymbols = [S0,S1,S2,S3,S4,S5,S6,S7,S8,S9]
# symbols used for expression equality check

x0, x1, x2, x3, x4, x5, x6, x7, x8, x9  = symbols(["x0","x1","x2","x3","x4","x5","x6","x7","x8","x9"])
_standardSymbols = [x0,x1,x2,x3,x4,x5,x6,x7,x8,x9]
# symbols used for expression representation only

_scalars = [0,1,2,3,4,5]

def normalizedExpr(expr):
    with evaluate(False):
        normalizedExpr = UnevaluatedExpr(expr)
        normExpr = normalizedExpr
        symbols = list(expr.free_symbols)
        i = 0
        for symbol in symbols:
            # switching to safe symbols
            normExpr = UnevaluatedExpr(normalizedExpr.subs(UnevaluatedExpr(symbol), UnevaluatedExpr(u._safeSymbols[i])))
            normalizedExpr = normExpr
            i = i+1
        i = 0
        for symbol in symbols:
            # returning to normalized symbols
            normExpr = UnevaluatedExpr(normalizedExpr.subs(UnevaluatedExpr(u._safeSymbols[i]), UnevaluatedExpr(u._standardSymbols[i])))
            normalizedExpr = normExpr
            i = i+1
    return normExpr

def switchSymbol(expr, symbol1, symbol2):
    # returns an expression with symbol1 replaced by symbol2
    # assumes symbol1 and symbol2 are different!
    exprSymbols = list(expr.free_symbols)
    check = (symbol2 in exprSymbols)
    if check == False:
        switchExpr = expr.subs(symbol1, symbol2, evaluate=False)
    else:
        print("symbol already present in expression")
        switchExpr = expr
    return switchExpr

def switchToSafeSymbols(expr,safeSyms):
    safeExpr = expr
    i = 0
    oldSymbols = list(expr.free_symbols)
    for s in oldSymbols:
        # safeExpr needs to have safe symbols S1,S2,...,SN to avoid chaos
        safeExpr = safeExpr.subs(s,safeSyms[i])
        i = i+1
    return safeExpr

def areExpressionsEqual(expr1, expr2):
    # this method checks if two expressions are equal in a structural sense
    # they are equal if there exists a symbol permutation that makes them equal
    check = False
    symbols1 = list(expr1.free_symbols)
    symbols2 = list(expr2.free_symbols)
    if len(symbols1) == len(symbols2):
        safeSyms = u._safeSymbols[0:len(symbols1)] 
        # the two expressions have the same number of symbols (N)
        safeExpr1 = switchToSafeSymbols(expr1,safeSyms)
        # now safeExpr1 has safe symbols S1,S2,...,SN.
        print(safeExpr1)
        print("checking permutations...")
        perms = list(tools.permutations(safeSyms))
        for perm in perms:
            #iterating through all permutations of symbols
            safeSyms2 = perm
            print(safeSyms2)
            safeExpr2 = switchToSafeSymbols(expr2,safeSyms2)
            print(safeExpr2)
            # checking if permutated safeExpr2 is equal to safeExpr1
            if (safeExpr1.expand() - safeExpr2.expand() == 0):
                check = True
                break
                # exiting loop
    else:
        print("expressions have different number of symbols")
        # check remains False
    return check

def treeToExpr(tree, node, args, numLeaves):
    # generates polynomial expressions
    with evaluate(False):
        children = tree.nodes[node]["children"]
        # gets number of children
        if children == 0:
            # leaf node. Append leaf to list
            # !!! ------------------------------------ how to choose variables and scalars? ------------------------------------- !!!
            # values = u._standardSymbols[0:len(leaves)-1] + u._scalars
            tree.nodes[node]["nodeType"] = "X"
            values = u._standardSymbols[0:numLeaves]
            args = UnevaluatedExpr(choice(values))
        elif children == 1:
            # unary operator. (multiplication by -1)
            for child in nx.neighbors(tree, node):
                #args = [Mul(*flatten([treeToExpr(tree, child, args),-1]),evaluate=False)]
                if choice([1,2]) == 1:
                    _exp = choice([0,1,2,3,4,5])
                    if _exp == 2:
                        tree.nodes[node]["nodeType"] = "Pow2"
                    else:
                        tree.nodes[node]["nodeType"] = "Pow"
                    args = [UnevaluatedExpr(Pow(*flatten([treeToExpr(tree, child, args, numLeaves),_exp]), evaluate=False))]
                else:
                    with evaluate(True):
                        tree.nodes[node]["nodeType"] = "Opp"
                        args = [UnevaluatedExpr(Mul(*flatten([treeToExpr(tree, child, args, numLeaves),-1])))]
        else:
            # n-ary operator. (Add or Mul)
            _args = []
            _op = choice([Add,Mul])
            if _op == Mul:
                tree.nodes[node]["nodeType"] = "Mul"
            else:
                tree.nodes[node]["nodeType"] = "Add"
            for child in nx.neighbors(tree, node):
                _args.append(treeToExpr(tree, child, args, numLeaves))
            args = [UnevaluatedExpr(_op(*flatten(_args)))]
    return args

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def exprLength(expr):
    return len(str(expr))

# ------------------------------------------------ SHAPE TEST ------------------------------------------------- #

def isPower(tree, root):
    check = False
    if tree.nodes[root]["nodeType"] == "Pow":
        check = True
    if tree.nodes[root]["nodeType"] == "Pow2":
        check = True
    return check

def isSquare(tree, root):
    check = False
    if tree.nodes[root]["nodeType"] == "Pow2":
        check = True
    return check

def isDifferenceOfSquares(tree, root):
    check = False
    if tree.nodes[root]["children"] == 2:
        if tree.nodes[root]["nodeType"] == "Add":
            for child in nx.neighbors(tree, root):
                check = True
                if isPower(tree, child) == False:
                    check = False
    return check

