#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

# Note: The provided code is unclean and lacks efficient performance!

def gen_params(p, h):
    F = GF(p ** h)
    R = PolynomialRing(GF(p), 'x')
    P = Permutations(p)
    r = P.random_element()

    while True:
        f = R.random_element(degree = h)
        if f.is_irreducible():
            f *= f.list()[-1] ** -1
            break

    g = F.gen()
    while True:
        _ = randint(1, p ** h - 1)
        if gcd(_, p ** h - 1) == 1:
            g = g ** _
            break

    RR.<x> = GF(p**h)[]
    f = RR(f)
    t = f.roots()[0][0]
    return g, t, r

def genkey(p, h, params):
    g, t, r = params
    pubkey, d = [], randint(1, p ** h - 1)
    P = Permutations(p)
    pi = P.random_element()
    for _ in range(p):
        b = discrete_log(t + r[pi[_] - 1] - 1, g)
        c = (b + d) % (p ** h - 1)
        pubkey.append(c)
    privkey = (d, pi, t, g)
    return pubkey, privkey

def encode(msg, p, h):
    m = bytes_to_long(msg)
    B = bin(m)[2:].zfill(8 * len(msg))
    BA = [B[i*h:(i+1)*h] for i in range(len(B) // h)]
    M = []
    for ba in BA:
        m = ba.ljust(p, '0')
        m = m[:-h + m.count('1')] + '1' * (h - m.count('1'))
        M.append(m)
    return M

def encrypt(msg, pubkey, p, h):
    M, C = encode(msg, p, h), []
    for m in M:
        s = 0
        for i in range(p):
            s += int(m[i]) * pubkey[i]
        C.append(s % (p ** h - 1))
    return C

p, h = 223, 24
params = gen_params(p, h)
g, t, r = params
pubkey, _ = genkey(p, h, params)
enc = encrypt(flag, pubkey, p, h)

print(f'r = {r}')
print(f'pubkey  = {pubkey}')
print(f'enc = {enc}')