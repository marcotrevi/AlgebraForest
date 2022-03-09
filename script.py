from datetime import timedelta
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt

#from random import choice, randint
#from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity

n = 6

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

x = symbols("x")

def treeToExpr(tree, node, args):
    children = tree.nodes[node]["children"] 
    if children == 0:
        # leaf node. Append leaf to list
        args = tree.nodes[node]["nodeID"]
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


expr = treeToString(T, root, "")
print(expr)

args = treeToExpr(T, root, [])
print(args)

value = args[0].doit()
print(value)

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

