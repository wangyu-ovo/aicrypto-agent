from Crypto.Util.number import *
from primefac import *
import gmpy2
from sympy import *
from helper import *

e = 0x10001
p = williams_pp1(n)
q_2 = gmpy2.invert(d, p ** 2)
# Find the solutions to ``x**n = a mod m`` when m is not prime.
q = nthroot_mod(q_2, 2, p ** 2)

r = n // p // q

fin = (p - 1) * (q - 1) * (r - 1)
di = gmpy2.invert(e, fin)
c = gmpy2.powmod(cipher, di, n)

m = nthroot_mod(c, 2, r)
print(long_to_bytes(m))