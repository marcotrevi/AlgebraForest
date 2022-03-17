from asyncio import WriteTransport
from datetime import timedelta
from math import remainder
import random as r
from secrets import choice
from sympy import *
import networkx as nx
import matplotlib.pyplot as plt
import itertools as tools
import utilities as u
import graphDBcommitter as neo
from csv import writer

def buildExpression(numNodes):
    treeList = list(nx.nonisomorphic_trees(numNodes, create="graph"))
    # this list contains all trees on "n" nodes
    expressions = []
    trees = []
    roots = []
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

        args = u.normalizedExpr(u.treeToExpr(T, root, [], len(leaves))[0])
        expressions.append(args)
        trees.append(T)
        roots.append(root)
        output = [expressions, trees, roots]
    return output

#expr = buildExpression(6)

singleTree = False
showPlot = False

if singleTree:
    numNodes = 6 
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

#print(args[0])
#normExpr = str(u.normalizedExpr(args[0]))
#print(normExpr)
#print(u.exprLength(args[0]))
#print(nx.get_node_attributes(T,"nodeType"))
#print(u.isPower(T, root))
#print(u.isSquare(T, root))
#print(u.isMul(T, root))
#print(u.isDifferenceOfSquares(T, root))

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

#row = [latex(args[0]), u.exprLength(args[0])]
#u.append_list_as_row('formulaDB.csv', row)

results = buildExpression(5)
# builds an expression for every n-node tree
exprList = results[0]
treeList = results[1]
rootList = results[2]
L = len(exprList)
#print(normExprList)
#print(treeList)
#print(rootList)

doneExpr = exprList[0].doit()
print(exprList[0])
print(doneExpr)


writeToGraph = False
_init = True
if writeToGraph:
    uri = "neo4j+s://cb231e56.databases.neo4j.io"
    user = "neo4j"
    password = "5631ZHUiFDJ1kLH96wfoVdCzdF4kAqKCwPiXgFwucKI"
    app = neo.App(uri, user, password)
    if _init:
        app.createOperationNode("ADD")
        app.createOperationNode("MUL")
        app.createOperationNode("POW")
        app.createOperationNode("OPP")
        app.createOperationNode("SQUARE_DIFF")
    i = 0
    for normExpr in exprList:
        remainder = L-i
        print("trees to go: "+str(remainder))
        expr = str(normExpr)
        T = treeList[i]
        root = rootList[i]
        app.createExpressionNode(expr)
        if u.isMul(T,root):
            app.create_dependency(expr,"MUL")    
        elif u.isDifferenceOfSquares(T,root):
            app.create_dependency(expr,"SQUARE_DIFF")
        elif u.isPower(T,root):
            app.create_dependency(expr,"POW")
        elif u.isAdd(T,root):
            app.create_dependency(expr,"ADD")
        elif u.isOpp(T,root):
            app.create_dependency(expr,"OPP")
        i = i+1
    app.close()