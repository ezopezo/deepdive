import math

def fact():
    for i in range(20000):
        yield math.factorial(i)

f = fact()

for j in f:
    print(j)