import sympy
from sympy import *
x,y = symbols("x y")
expr1 = cos(x)
expr2 = sin(x)
print(expr1.subs(x,expr2).subs(x,0))