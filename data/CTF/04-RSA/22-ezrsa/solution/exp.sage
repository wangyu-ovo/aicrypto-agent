from gmpy2 import *
from Crypto.Util.number import *
from libnum import *
import random
from helper import *
e = 0x10001
f = enc.strip().split('n')
cipher = [i for i in f]
cipher = cipher[:-1]
cipher = [int(i) for i in cipher]
flag = ""
for i in cipher:
    if jacobi(i,n1)==-1:
        flag += '0'
    else:
        flag += '1'

p = int(flag[::-1],2)
print('p = '+str(p))
def attack(c1, c2, noise1, noise2,  e1, e2 , n):
    
    PR.<x>=PolynomialRing(Zmod(n))
    g1 = (x + noise1)^e1 - c1
    g2 = (x + noise2)^e2 - c2

    def gcd(g1, g2):
        while g2:
            g1, g2 = g2, g1 % g2
        return g1.monic()
    print(gcd(g1, g2))
    return -gcd(g1, g2)[0]

q = int(attack(c1, c2, noise1, noise2,  e1, e2 , n2))
print('q = ' +str(q))
n = p*q
phi = (p-1)*(q-1)
d = inverse_mod(e,phi)
m = power_mod(c,d,n)
print(long_to_bytes(m))