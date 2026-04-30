ells = [*primes(3, 128), 163]
p = 4 * prod(ells) - 1
print(pari.quadclassunit(-4*p))

order = 102019419125180345266808265
q3 = pari.Qfb(3, 2, (p + 1) // 3)
assert q3^order == q3^0

from tqdm import tqdm

dlogs = []
for ell in tqdm(ells[1:]):
    qfb = pari.Qfb(ell, 2, (p + 1) // ell)
    dlog = discrete_log(qfb, q3, order, operation=None, identity=q3^0, inverse=lambda x:x^-1, op=lambda a,b:a*b, algorithm='lambda')
    dlogs.append(dlog)
print(f'{dlogs = }')

M = matrix(32)
M[0, 0] = order
M[1:-1, 1:-1] = identity_matrix(30)
M[1:-1, 0] = -vector(dlogs)
M[-1, -2] = mod(1/2, order)
M[-1, -1] = 2^1024 # Kannan embedding with large weight

# .change_ring(ZZ).LLL()
print(M.LLL()[-1][:-1])

from ast import literal_eval
from hashlib import sha256
from Crypto.Cipher import AES

ells = [*primes(3, 128), 163]
p = 4 * prod(ells) - 1
F = GF(p)

def csidh(A, priv):
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    for sgn in [1, -1]:
        for e, ell in zip(priv, ells):
            for i in range(sgn * e):
                while not (P := (p + 1) // ell * E.random_element()):
                    pass
                E = E.isogeny_codomain(P)
        E = E.quadratic_twist()
    return E.montgomery_model().a2()

# This is the private key for the 163-isogeny, given by [0, 0, ..., 0, 1]
priv_163 = [int(ell == 163) for ell in ells]
pub_163 = csidh(0, priv_163)

# This is the private key for the sqrt(163)-isogeny, such that if you square it you get the 163-isogeny
priv_rt163 = M.LLL()[-1][:-1]
pub_rt163 = csidh(0, priv_rt163)

assert csidh(pub_rt163, priv_rt163) == pub_163, "Your private key does not define a sqrt(163)-isogeny!"
load('./helper.sage')
print(AES.new(sha256(str(pub_rt163).encode()).digest(), AES.MODE_ECB).decrypt(bytes.fromhex(ct)).decode())