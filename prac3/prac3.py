"""
#1. whitespace before '('
def f ():
    print("Hello")
f()

#2. missing whitespace arount operator
print(5+ 4)

#3. missing whitespace after ','
print([2,3,4])

#4. unexpected spaces around keyword / parameter equals
def f(arg=0):
    return 2**arg
f(arg = 2)

#5. expected 2 blank lines, found 1
def f1():
    return "Hello"

def f2():
    return "World"

#6. multiple statements on one line (color)
if True: print("hello")

#7. multiple statements on one line (semicolon)
print("hello"); print("world")

#8. comparison to None should be 'if cond is None:'
def f(x):
    if x % 2 == 0:
        return True

r = f(x)

if r == None:
    print("odd")

#9. comparison to True should be 'if cond is True:' or 'if cond:'
def f(x):
    if x % 2 == 0:
        return True

r = f(x)

if r == True:
    print("even")

"""
from printermodule import *

try:
	hello() # hello
	world() # world
except:
	pass 

import helloworldpkg.hello
import helloworldpkg.world

helloworldpkg.hello.printh()
helloworldpkg.world.printw()

import logging
import traceback

logging.basicConfig(filename='logfile.log', filemode='w', level=logging.INFO)
logging.raiseExceptions = True

def div(a, b):
	try:
		return a/b, None
	except Exception as e:
		return e, traceback.format_exc()

def run_with_log(func, a, b):
	out, trace = div(a,b)
	if trace is not None:
		return logging.exception(f'{out}\n{trace}')

run_with_log(div, 6, 3)
run_with_log(div, 6, 0)
run_with_log(div, "5", 2)