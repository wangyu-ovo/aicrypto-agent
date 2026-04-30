from Crypto.Util.number import *
from gmpy2 import *
from secret import flag


def gen():
    p1 = getPrime(256)
    while True:
        f = getRandomRange(1, iroot(p1 // 2, 2)[0])
        g = getRandomRange(iroot(p1 // 4, 2)[0], iroot(p1 // 2, 2)[0])
        if gcd(f, p1) == 1 and gcd(f, g) == 1 and isPrime(g) == 1:
            break
    rand = getRandomRange(0, 2 ^ 20)
    g1 = g ^^ rand
    h = (inverse(f, p1) * g1) % p1
    return h, p1, g, f, g1


def gen_irreducable_poly(deg):
    while True:
        out = R.random_element(degree=deg)
        if out.is_irreducible():
            return out


h, p1, g, f, g1 = gen()
q = getPrime(1024)
n = g * q 
e = 0x10001
c1 = pow(bytes_to_long(flag), e, n)
hint = list(str(h))
length = len(hint)
bits = 16
p2 = random_prime(2 ^ bits - 1, False, 2 ^ (bits - 1))
R.<x> = PolynomialRing(GF(p2))
P = gen_irreducable_poly(ZZ.random_element(length, 2 * length))
Q = gen_irreducable_poly(ZZ.random_element(length, 2 * length))
N = P * Q
S.<x> = R.quotient(N)
m = S(hint)
c2 = m ^ e
print("p1 =", p1)
print("c1 =", c1)
print("p2 =", p2)
print("c2 =", c2)
print("n =", n)
print("N =", N)


