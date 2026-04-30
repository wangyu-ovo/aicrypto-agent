#!/usr/bin/env python3

from Crypto.Util.number import *
from math import sqrt
from flag import flag

def gen_params(nbit):
    p, Q, R, S = getPrime(nbit), [], [], []
    d = int(sqrt(nbit << 1))
    for _ in range(d):
        Q.append(getRandomRange(1, p - 1))
        R.append(getRandomRange(0, p - 1))
        S.append(getRandomRange(0, p - 1))
    return p, Q, R, S

def encrypt(m, params):
    p, Q, R, S = params
    assert m < p
    d = int(sqrt(p.bit_length() << 1))
    C = []
    for _ in range(d):
        r, s = [getRandomNBitInteger(d) for _ in '01']
        c = Q[_] * m + r * R[_] + s * S[_]
        C.append(c % p)
    return C


nbit = 512
params = gen_params(512)
m = bytes_to_long(flag)
C = encrypt(m, params)
f = open('params_enc.txt', 'w')
f.write(f'p = {params[0]}\n')
f.write(f'Q = {params[1]}\n')
f.write(f'R = {params[2]}\n')
f.write(f'S = {params[3]}\n')
f.write(f'C = {C}')
f.close()