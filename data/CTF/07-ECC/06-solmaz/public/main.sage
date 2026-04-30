#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def gen_param(nbit):
    while True:
        t = prod([getPrime(nbit >> 3) for _ in range(4)])
        p = 4 * t ** 2 + 1
        if is_prime(p):
            c = randint(3, p - 3) ** 2 % p
            E = EllipticCurve(GF(p), [c, 0])
            if E.order() == p - 1:
                return p, c

def encrypt(m, x, p, c):
    E = EllipticCurve(GF(p), [c, 0])
    while True:
        try:
            P = E.lift_x(x)
            break
        except:
            x += 1
    assert m < p - 1
    Q = m * P
    return P, Q, m

nbit, x = 256, 1337
m = bytes_to_long(flag.lstrip(b'CCTF{').rstrip(b'}'))
p, c = gen_param(nbit)
P, Q, m = encrypt(m, x, p, c)

print(f'P = {P.x(), P.y()}')
print(f'Q = {Q.x(), Q.y()}')