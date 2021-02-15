import math

def f14(n):
    if(n<0):
        return None
    elif(n==0):
        return 2
    elif(n==1):
        return 10
    else:
        return 1/67*f14(n-2) + math.cos(f14(n-2))
