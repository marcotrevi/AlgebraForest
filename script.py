from datetime import timedelta
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt

#from random import choice, randint
#from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity

n = 3

print('start')
T = nx.nonisomorphic_trees(n, create="graph")
g = list(T)
print('stop')

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

x,y,z = symbols(["x","y","z"])
sym = [x,y,z]
num = []
vars = sym + num

def treeToExpr(tree, node, args):
    children = tree.nodes[node]["children"] 
    if children == 0:
        # leaf node. Append leaf to list
        # args = tree.nodes[node]["nodeID"]
        args = choice(vars)
    elif children == 1:
        # unary operator. (multiplication by -1)
        for child in nx.neighbors(tree, node):
            args = [Mul(*flatten([treeToExpr(tree, child, args),-1]),evaluate=False)]
        #print(args)
    else:
        # n-ary operator. (Add or Mul)
        _args = []
        ops = [Add,Mul]
        for child in nx.neighbors(tree, node):
            _args.append(treeToExpr(tree, child, args))
            #print(_args)
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

#expr = treeToString(T, root, "")
#print(expr)

args = treeToExpr(T, root, [])
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

def areExpressionsEqual(expr1, expr2):
    check = False
    symbols1 = list(expr1.free_symbols)
    symbols2 = list(expr2.free_symbols)
    if len(symbols1) == len(symbols2):
        if symbols1 == symbols2:
            print("ok - go with the permutations")
            # both expressions have the same symbol set
        else:
            print("building same set of symbols for both expressions")
    else:
        print("expressions have different number of symbols")
    return check

print()

# checking if two expressions are equal
# expr1 = UnevaluatedExpr(x)*(UnevaluatedExpr(x)+UnevaluatedExpr(y))
expr1 = x+y
expr2 = y+z
print(areExpressionsEqual(expr1, expr2))
# print(expr1)
# print(switchSymbol(expr1, x, z))


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

#plt.show()

