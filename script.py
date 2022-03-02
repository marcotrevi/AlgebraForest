from datetime import timedelta
import random as r
import sympy
from sympy import *
import utilities as U
import networkx as nx
import matplotlib.pyplot as plt

#from random import choice, randint
#from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity

n = 6

print('start')
T = nx.nonisomorphic_trees(n, create="graph")
print('stop')

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

children = {}
# children dictionary
for i in T.nodes:
    N = [n for n in T.neighbors(i)]
    children[i] = len(N)

nx.set_node_attributes(T, children, name="children")
# nodes have number of children as attribute

nodeType = {}
# operation or symbol
for i in T.nodes:
    n_children = T.nodes[i]["children"] 
    if n_children == 0:
        nodeType[i] = 'L'
    else:
        nodeType[i] = 'OP' + str(n_children)

nx.set_node_attributes(T, nodeType, name="node type")
# nodes have node type as attribute

_bfs = nx.bfs_successors(T,root)
print(dict(_bfs))

def treeToExpression(tree, node):
    # converting tree into sympy expression
    # gets a tree graph in networkx and returns a sympy expression
    types = [Add, Mul]
    if tree.nodes[node]["node type"] == 'L':
        expr = symbols('x')
        expr = UnevaluatedExpr(expr)
    elif tree.nodes[node]["node type"] == 'OP1':
        for j in nx.neighbors(tree,node):
            nn = j
        print(j)
        expr = -UnevaluatedExpr(treeToExpression(tree, nn))
    else:
        args = []
        for i in nx.neighbors(tree, node):
            args.append(treeToExpression(tree, i))
        #expr = r.choice(types)(*args, evaluate=False)
        expr = Add(*args)
    return expr

expr = treeToExpression(T, root)
print(expr)

color_map = []
for node in T:
    if node == root:
        color_map.append('red')
    else: 
        color_map.append('blue')

#labels = nodeType
nx.draw_networkx_nodes(T, pos, node_size=1000, node_color=color_map)
nx.draw_networkx_edges(T, pos, edgelist=T.edges(), edge_color='black')
nx.draw_networkx_labels(T, pos, labels, font_color='white')

plt.show()

