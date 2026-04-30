#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import *
from secret import d, flag

def genkey(d):
    while True:
        f = getRandomRange(1, int(sqrt(2) * 10 ** d))
        g = getRandomRange(10 ** d, int(sqrt(2) * 10 ** d))
        if gcd(f, 10 * g) == 1:
            q = 4 * 100 ** d
            h = inverse(f, q) * g % q
            if gcd(h, 10 * d) == 1:
                break
    pkey, skey = (d, h), (f, g)
    return pkey, skey

def encrypt(m, pkey):
    d, h = pkey
    q = 4 * 100 ** d
    assert m < 10 ** d
    r = getRandomRange(1, 10 ** d // 2)
    c = (r * h + m + r) % q
    return c

pkey, _ = genkey(d)
m = bytes_to_long(flag)
c = encrypt(m, pkey)

print(f'h = {pkey[1]}')
print(f'c = {c}')