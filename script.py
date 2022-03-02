from datetime import timedelta
from random import *
import sympy
from sympy import *
import utilities as U
import networkx as nx
import matplotlib.pyplot as plt

#from random import choice, randint
#from sympy import FunctionClass, Add, Mul, cos, sin, binomial, arity

def treeToExpression(tree):
    # gets a tree graph in networkx and returns a sympy expression
    expr = tree
    return expr

n = 6

print('start')
T = nx.nonisomorphic_trees(n, create="graph")
print('stop')

g = list(T)
k = 4
G = g[k]
# G is a tree graph

pos = nx.spring_layout(G)

# dictionary comprehension
labels = {x:x for x in range(n)}
root = 5

T = nx.bfs_tree(G,root)
# builds a digraph (BFS tree)
# now neighbors of a node are only children



nx.draw_networkx_nodes(T, pos, node_size=500)
nx.draw_networkx_edges(T, pos, edgelist=T.edges(), edge_color='black')
nx.draw_networkx_labels(T, pos, labels, font_color='white')
plt.show()