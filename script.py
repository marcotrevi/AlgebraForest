from datetime import timedelta
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt
import itertools as tools
import utilities as u
from csv import writer

def buildExpression(numNodes):
    treeList = list(nx.nonisomorphic_trees(numNodes, create="graph"))
    # this list contains all trees on "n" nodes
    expressions = []
    for _tree in treeList:
        root = r.randint(0,numNodes-1)
        T = nx.bfs_tree(_tree,root)
        # builds a digraph (BFS tree)

        leaves = [node for node in T.nodes() if T.out_degree(node)==0 and T.in_degree(node)==1]

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

        args = u.treeToExpr(T, root, [], len(leaves))
        showPlot = False
        if showPlot:
            #labels = nodeType
            color_map = []
            for node in T:
                if node == root:
                    color_map.append('red')
                else: 
                    color_map.append('blue')
            pos = nx.spring_layout(T)
            nx.draw_networkx_nodes(T, pos, node_size=500, node_color=color_map)
            nx.draw_networkx_edges(T, pos, edgelist=T.edges(), edge_color='black')
            nx.draw_networkx_labels(T, pos, labels, font_color='white')
            plt.show()
        expressions.append(args)
    return expressions

#expr = buildExpression(6)

numNodes = 8
showPlot = False

treeList = list(nx.nonisomorphic_trees(numNodes, create="graph"))
# this list contains all trees on "n" nodes
_tree = treeList[r.randint(0,len(treeList)-1)]
root = r.randint(0,numNodes-1)
# selects random node as root
T = nx.bfs_tree(_tree,root)
# builds a digraph (BFS tree)

leaves = [node for node in T.nodes() if T.out_degree(node)==0 and T.in_degree(node)==1]

labels = {x:x for x in T.nodes}
# label dictionary

children = {}
# children dictionary
for i in T.nodes:
    N = [n for n in T.neighbors(i)]
    children[i] = len(N)

# nodes have number of children as attribute

nodeType = {}
# operation or symbol dictionary
for i in T.nodes:
    nodeType[i] = ""

nx.set_node_attributes(T, children, name="children")
nx.set_node_attributes(T, labels, name="nodeID")
nx.set_node_attributes(T, nodeType, name="nodeType")

args = u.treeToExpr(T, root, [], len(leaves))

nodeType = nx.get_node_attributes(T,"nodeType")

print(args[0])
print(u.normalizedExpr(args[0]))
print(u.exprLength(args[0]))
print(nx.get_node_attributes(T,"nodeType"))
print(u.isPower(T, root))
print(u.isSquare(T, root))
print(u.isDifferenceOfSquares(T, root))

if showPlot:
    #labels = nodeType
    color_map = []
    for node in T:
        if node == root:
            color_map.append('red')
        else: 
            color_map.append('blue')
    pos = nx.spring_layout(T)
    nx.draw_networkx_nodes(T, pos, node_size=700, node_color=color_map)
    nx.draw_networkx_edges(T, pos, edgelist=T.edges(), edge_color='black')
    nx.draw_networkx_labels(T, pos, nodeType, font_color='white')
    plt.show()

row = [latex(args[0]), u.exprLength(args[0])]
u.append_list_as_row('formulaDB.csv', row)


