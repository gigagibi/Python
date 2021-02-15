import math

def f12(x):
    if(x<105):
        return x**2 + x**3 + 88
    elif(x >= 105 and x < 180):
        return ((47*x**7 + math.sin(x))**3)/71 + x**4
    elif(x >= 180 and x < 259):
        return x**6+x
    elif(x>=259):
        return x**7-39*x**4