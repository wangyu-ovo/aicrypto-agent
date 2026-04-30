#!/usr/bin/env sage

from Crypto.Util.number import *
from secret import b, g, flag

def encrypt(m, b, g):
    i, c = 0, 0
    while True:
        N, D = b * g, n(pow(g, Rational(2*i/m)), prec = b) + g
        s = N/D
        c += s
        i += 1
        if i >= m:
            return c

m = bytes_to_long(flag.lstrip(b'CCTF{').rstrip(b'}'))
c = encrypt(m, b, g)
# Takes many many years :(
print(f'c = {c}')