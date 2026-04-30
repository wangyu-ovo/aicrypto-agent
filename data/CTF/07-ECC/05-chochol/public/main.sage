#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def keygen(nbit):
    while True:
        p, q = [getPrime(nbit) for _ in range(2)]
        if p % 4 == q % 4 == 3 and p < q:
            a = randint(1, p - 1)
            Ep, Eq = EllipticCurve(GF(p), [a, 0]), EllipticCurve(GF(q), [a, 0])
            try:
                Gp, Gq = Ep.lift_x(2024), Eq.lift_x(2024)
                s = randint(1, p)
                Hp, Hq = s * Gp, s * Gq
                pkey = (Gp, Hp, Gq, Hq)
                skey = (p, q, s)
                return pkey, skey
            except:
                continue

pkey, skey = keygen(128)
p, q, s = skey
n = p * q
m = bytes_to_long(flag.lstrip(b'CCTF{').rstrip(b'}'))
assert m < n
c = pow(m, s, n)

print(f'Gp = {pkey[0].xy()}')
print(f'Hp = {pkey[1].xy()}')
print(f'Gq = {pkey[2].xy()}')
print(f'Hq = {pkey[3].xy()}')
print(f'c  = {c}')