import gmpy2
from Crypto.Util.number import long_to_bytes
from helper import *

n1 = N1
n2 = N2
n3 = N3
c1 = ct1
c2 = ct2
c3 = ct3

N = n1*n2*n3
N1 = N // n1
N2 = N // n2
N3 = N // n3


u1 = gmpy2.invert(N1, n1)
u2 = gmpy2.invert(N2, n2)
u3 = gmpy2.invert(N3, n3)

M = (c1*u1*N1 + c2*u2*N2 + c3*u3*N3) % N

m = gmpy2.iroot(M,e)[0]

print(long_to_bytes(m))