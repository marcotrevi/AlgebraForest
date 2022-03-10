from datetime import timedelta
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt
import itertools as tools
import utilities as u

n = 8
T = nx.nonisomorphic_trees(n, create="graph")
g = list(T)

k = r.randint(0,len(g)-1)
root = r.randint(0,n-1)
G = g[k]
# G is a tree graph

pos = nx.spring_layout(G)

T = nx.bfs_tree(G,root)
# builds a digraph (BFS tree)
# now neighbors of a node are only children
# dictionary comprehension

labels = {x:x for x in T.nodes}
# label dictionary
nx.set_node_attributes(T, labels, name="nodeID")

children = {}
# children dictionary
for i in T.nodes:
    N = [n for n in T.neighbors(i)]
    children[i] = len(N)

nx.set_node_attributes(T, children, name="children")
# nodes have number of children as attribute

nodeType = {}
# operation or symbol dictionary
for i in T.nodes:
    n_children = T.nodes[i]["children"] 
    if n_children == 0:
        nodeType[i] = 'L'
    else:
        nodeType[i] = 'OP' + str(n_children)

nx.set_node_attributes(T, nodeType, name="node type")
# nodes have node type as attribute

def treeToExpr(tree, node, args):
    children = tree.nodes[node]["children"] 
    if children == 0:
        # leaf node. Append leaf to list
        args = choice(u._standardSymbols[0:3])
    elif children == 1:
        # unary operator. (multiplication by -1)
        for child in nx.neighbors(tree, node):
            args = [Pow(*flatten([treeToExpr(tree, child, args),2]),evaluate=False)]
            #args = [Mul(*flatten([treeToExpr(tree, child, args),-1]),evaluate=False)]
    else:
        # n-ary operator. (Add or Mul)
        _args = []
        ops = [Add,Mul]
        for child in nx.neighbors(tree, node):
            _args.append(treeToExpr(tree, child, args))
        args = [choice(ops)(*flatten(_args),evaluate=False)]
    return args

def treeToString(tree, node, string):
    string = str(tree.nodes[node]["nodeID"])
    children = tree.nodes[node]["children"] 
    if children == 0:
        # we are on a leaf node
        print("leaf")
    else:
        string = string + "("
        for child in nx.neighbors(tree, node):
            string = string + str(treeToString(tree, child, string)) + ","
        string = string + ")"
    return string

args = treeToExpr(T, root, [])
print("expression:")
print(args)

value = args[0].doit()
print(value)

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

print()

expr1 = (u.x1+u.y)*u.x
expr2 = u.x1*u.x+u.y*u.x1
print(areExpressionsEqual(expr1, expr2))

color_map = []
for node in T:
    if node == root:
        color_map.append('red')
    else: 
        color_map.append('blue')

#labels = nodeType
nx.draw_networkx_nodes(T, pos, node_size=500, node_color=color_map)
nx.draw_networkx_edges(T, pos, edgelist=T.edges(), edge_color='black')
nx.draw_networkx_labels(T, pos, labels, font_color='white')

plt.show()

