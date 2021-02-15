import math

def f13(n):
    sum1, sum2 = 0, 0
    for i in range(1, n+1):
        sum1 += (6*i**2-math.cos(i))
        sum2 += (i**7+86*i)
    return sum1 - sum2/98
