from Crypto.Util.number import *

data = open('./cts.txt', 'r').read()
cts = eval(data)

def two_dim_crt(c1, c2, n1, n2):
    k1 = pow(n1, -1, n2)
    k2 = pow(n2, -1, n1)
    return c1*k2*n2 + c2*k1*n1

def multi_dim_crt(cs, ns):
    i = 1
    c1 = cs[i-1]
    n1 = ns[i-1]
    while i < len(ns):
        c2 = cs[i]
        n2 = ns[i]
        c1 = two_dim_crt(c1, c2, n1, n2)
        n1 *= n2
        i += 1
    return c1

from functools import reduce
ns = [ct[0] for ct in cts]
N = reduce(lambda a, b: a*b, ns)
P.<x> = PolynomialRing(Zmod(N))
polys = []
for n, e, c, r in cts:
    r = int.from_bytes(r, "big")
    poly = (2^(16*8) * x + r)^e - c
    polys.append(poly)

combined = multi_dim_crt(polys, ns).monic()
root = combined.small_roots(X=2^432, beta=1, epsilon=1/16)[0]
print(long_to_bytes(int(root)))
