#!/usr/bin/env sage

from hashlib import sha256

def gen_params(m):
    C = CyclotomicField(m)
    F, PHI = C.maximal_totally_real_subfield()
    d = F.degree()
    D = [[0 for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for j in range(i + 1):
            if (i - j) % 2 == 0: D[i][j] = binomial(i, (i - j) >> 1)
    D = Matrix(D)
    O = [F(_) for _ in D.inverse()]
    return (C, F, PHI, O, D)

def genkey(F, O, D, _B):
    _d, g = F.degree(), F.gen()
    a = sum([randint(-_B, _B + 1) * g**_ for _ in range(_d)])
    A = a.matrix().LLL()
    while True:
        b = sum([randint(-_B, _B + 1) * g**_ for _ in range(_d)])
        B = b.matrix().LLL()
        C = block_matrix([[A], [B]]).change_ring(ZZ)
        R, M = C.hermite_form(transformation = True)
        if R[0:_d] == identity_matrix(_d): break
    c, d = F(-M[0][_d:2*_d]*B) / b, F(M[0][0:_d]*A) / a
    n = (a*c + b*d) / (a**2 + b**2)
    N = vector(n) * D
    _n = sum(round(N[_]) * O[_] for _ in range(_d))
    _c, _d = c - _n * a, d - _n * b
    skey = Matrix([[a, _c], [b, _d]])
    pkey = (skey + identity_matrix(2)) * (skey.T - identity_matrix(2))
    return (skey, pkey)

nbit = 4 * 32
C, F, PHI, O, D = gen_params(nbit)
skey, pkey = genkey(F, O, D, nbit >> 2)

flag = str(sum(skey.coefficients()).polynomial()(2^128))
flag = 'CCTF{' + sha256(flag.encode()).hexdigest() + '}'

f = open('flag_update.txt', 'w')
f.write(flag)
f.close()

f = open('pubkey_update', 'wb')
f.write(str(pkey).encode())
f.close()