#!/usr/bin/env sage

from Crypto.Util.number import *
from string import printable as prn

def genimen(k, p, _B):
    while True:
        A = random_matrix(GF(p), k)
        for i in range(k):
            for j in range(k):
                A[i, j] = int(A[i, j]) % (_B + 1)
        if det(A) != 0: return A

def genkey(k, p, _B, l):
    sA = [genimen(k, p, _B) for _ in range(l + 1)]
    L = list(range(l))
    shuffle(L)
    s, pE = randint(1, p - 1), prod([sA[_] for _ in L])
    sD, sE = sA[-1], s * pE
    pkey = [sE * _ * sD * sE.inverse() for _ in sA[:-1]], sA[:-1], pE
    skey = L, s, sE, sD
    return pkey, skey

def encrypt(pkey, _p):
    pA, psA, pE = pkey
    k = pA[0].nrows()
    C = identity_matrix(GF(p), k)
    for i in _p: C *= pA[i]
    return C

nbit = 256
k, l, p, _B = 5, 19, getPrime(nbit), 63
_p = list(range(l))
shuffle(_p)
flag = 'CCTF{' + ''.join([prn[10 + _p[_]] for _ in range(l)]) + '}'

pkey, skey = genkey(k, p, _B, l)
C = encrypt(pkey, _p)
print(f'pkey = {pkey}')
print(f'C = {C}')