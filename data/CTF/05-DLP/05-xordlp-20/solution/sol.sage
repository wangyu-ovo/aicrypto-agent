##!/usr/bin/env sage
import hashlib
from Crypto.Util.number import long_to_bytes
from tqdm import *
from helper import *

n = p
c_l = c
c = 9

def v2s(v):
    ret = []
    for _ in range(256):
        if v & 1:
            ret.append(-1)
        else:
            ret.append(1)
        v >>= 1
    return vector(ZZ, ret)

_cs = []
for i in range(256):
    _cs.append(power_mod(c, 2^i, n))

_cs = vector(ZZ, _cs)

M = []
_ms = []
for i in tqdm(range(256)):
    v = k[i]
    _m = c_l[i]
    s = v2s(v)
    M.append(s)
    for i in range(256):
        if s[i] == -1:
            _m *= power_mod(_cs[i], -1, n)
            _m %= n

    _ms.append(_m)

M = matrix(ZZ, M)

b_d = ""
for i in tqdm(range(256)):
    target = [0 for j in range(i)] + [1] + [0 for j in range(256 - i - 1)]
    target = vector(ZZ, target)
    x = M.solve_left(target)
    denoms = set()
    for y in x:
        denoms.add(y.denom())
    max_denom = max(denoms)
    x = max_denom * x
    c_d = 1
    for j in range(256):
        c_d *= power_mod(_ms[j], int(x[j]), n)
        c_d %= n
    if c_d != 1:
        b_d = "1" + b_d
    else:
        b_d = "0" + b_d

x = int(b_d, 2)

print(x)
FLAG = bytes([i ^^ j for (i,j) in zip(enc, hashlib.sha384(long_to_bytes(x)).digest())])
print(FLAG)