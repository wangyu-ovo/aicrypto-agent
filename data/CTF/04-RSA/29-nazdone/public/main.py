#!/usr/bin/env python3

from Crypto.Util.number import *
from random import *
from secret import params, flag

def sol(m, a, z):
    p = m * (a - 1) % 2 + 1
    while True:
        R = list(range(1, a))
        shuffle(R)
        for r in R[:z]:
            p += getRandomRange(0, 2) * m ** r
        if isPrime(p):
            return p
        else:
            p = m * (a - 1) % 2 + 1


p, q, r = [sol(*params) for _ in '007']
n = p * q * r
m = bytes_to_long(flag)
c = pow(m, params[0] ** 3 + params[2] - 2, n)
print(f'n = {n}')
print(f'c = {c}')