import sympy
import random

def myGetPrime():
    A= getPrime(513)
    print(A)
    B=A-random.randint(1e3,1e5)
    print(B)
    return sympy.nextPrime((factorial(B))%A)

p=myGetPrime()

q=myGetPrime()

r=myGetPrime()

n=p*q*r

c=pow(flag,e,n)
