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

x,y,z = symbols(["x","y","z"])
# creating expression (x+y)*z
expr = [[1,2],[3,4]]
expr = [Add(*flatten(expr), evaluate=False)]
print(expr)






