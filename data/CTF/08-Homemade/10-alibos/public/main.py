#!/usr/bin/env python3

from Crypto.Util.number import *
from gmpy2 import *
from secret import d, flag

get_context().precision = 1337

def pad(m, d):
    if len(str(m)) < d:
        m = str(m) + '1' * (d - len(str(m)))
    return int(m)

def genkey(d):
    skey = getRandomRange(10 ** (d - 1), 10 ** d)
    pkey = int(10**d * (sqrt(skey) - floor(sqrt(skey))))
    return pkey, skey

def encrypt(m, pkey):
    m = pad(m, len(str(pkey)))
    d = len(str(pkey))
    c = (pkey + d ** 2 * m) % (10 ** d)
    return c

pkey, skey = genkey(d)

m = bytes_to_long(flag)
c = encrypt(m, pkey)

print(f'pkey = {pkey}')
print(f'enc  = {c}')