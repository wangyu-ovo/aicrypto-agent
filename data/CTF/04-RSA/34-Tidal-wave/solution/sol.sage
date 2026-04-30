from helper import *

R = Zmod(N)
n, k = 36, 8
prime_bit_length = 512

def make_G(R, alphas):
    mat = []
    for i in range(k):
        row = []
        for j in range(n):
            row.append(alphas[j]^i)
        mat.append(row)
    mat = matrix(R, mat)
    return mat

def get_alphas():
    PR = PolynomialRing(R,"x",n)
    xs = PR.gens()
    length = k
    l = 1
    polys = []
    for l in range(5):
        print("---", l, "---")
        offset = l * 7
        poly = 1
        for i in range(length):
            for j in range(0, i):
                poly *= (xs[i+offset] - xs[j+offset])
        poly -= dets[l]
        polys.append(poly)

        for i in range(n):
            x2s = []
            for i in range(length):
                polys.append(xs[i+offset]^2 - double_alphas[i+offset])

    I = ideal(polys)
    basis = I.groebner_basis()
    param_sum = 0
    coefficients = []
    for i in range(1, len(basis)):
        param_sum += -basis[i].coefficient(xs[-1])
        coefficients.append(-basis[i].coefficient(xs[-1]))

    param_sum += 1

    last_alpha = alpha_sum_rsa / (param_sum^65537) / pow(double_alphas[-1], 32768)
    predict_alphas = []

    for c in coefficients:
        predict_alphas.append(c*last_alpha)
    predict_alphas.append(last_alpha)

    return predict_alphas

def get_p(alphas):
    error_range = 2^1000
    G = make_G(R, alphas)
    r = p_encoded

    GZZ = G.change_ring(ZZ)
    NI = (N) * matrix.identity(ZZ, n)
    Ik = matrix.identity(ZZ, k)
    Zero = matrix(ZZ, n, k)

    step = ceil(prime_bit_length/k)

    # [m1, m2, ..., mk, k1, k2, ..., kn]
    mat = block_matrix(
        [
            [GZZ      , Ik       ],
            [NI       , Zero     ]
        ]
    )

    lb = [ZZ(r[i]) - error_range for i in range(n)] + [0 for i in range(k)]
    ub = [ZZ(r[i]) + error_range for i in range(n)] + [2**step for i in range(k)]
    load("./rkm.sage")
    result, applied_weights, fin = solve(mat, lb, ub)

    pbar = 0
    for i in range(k):
        pbar += R(fin[i] * 2^(step*i))

    PR.<x> = PolynomialRing(R)
    f = x + pbar
    x0 = f.small_roots(X=2^step, beta=0.3)[0]
    return ZZ(x0 + pbar)

def test_p(p, c, alphas):
    F = GF(p)
    alphas = alphas.change_ring(F)

    l = []
    for i in range(n):
        l.append(F(i))
    row = []

    G = make_G(F, alphas)

    C = codes.GeneralizedReedSolomonCode(alphas, k)

    return C.decode_to_message(c)

def get_keyvec(alphas, p, q):
    R = Zmod(N)
    G = make_G(R, alphas)
    from helper import key_encoded
    key_encoded = vector(key_encoded)
    alphas = vector(alphas)

    mp = test_p(p, key_encoded, alphas).change_ring(ZZ)
    mq = test_p(q, key_encoded, alphas).change_ring(ZZ)

    mm = []
    for i in range(len(mp)):
        mm.append(crt([mp[i], mq[i]], [p, q]))

    return vector(mm)

alphas = get_alphas()
p = ZZ(get_p(alphas))
q = ZZ(N // p)
print(f"{p=}")
keyvec = get_keyvec(alphas, p, q)

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
key = hashlib.sha256(str(keyvec).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
flag = cipher.decrypt(encrypted_flag)
print(flag)