from sympy import nextprime
from helper import *
from Crypto.Util.number import *
from gmpy2 import invert

def get_p_q(A,B):
    tmp = 1
    # calculate remain value (mod A) of (A−1)(A−2)(A−3)...(B+1)
    for i in range(B+1,A-1):
        tmp *= i
        tmp %= A

    tmp_inv = invert(tmp,A)
    result = nextprime(tmp_inv)
    return result

p = get_p_q(A1,B1)
q = get_p_q(A2,B2)
print(p)
print(q)
r = n // p // q
print(r)
phn = (p - 1) * (q - 1) * (r - 1)
d = invert(e, phn)
print(d)
m = pow(c,d,n)
print(m)
print(long_to_bytes(m))
