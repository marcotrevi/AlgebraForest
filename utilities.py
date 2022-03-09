from sympy import *

def sumExpr(x,y):
    return x+y

def prodExpr(x,y):
    return x*y

def powExpr(x,y):
    return x**y

def buildExpr(type, x ,y):
    if(type == 1):
        return x+y
    elif(type == 2):
        return x*y

