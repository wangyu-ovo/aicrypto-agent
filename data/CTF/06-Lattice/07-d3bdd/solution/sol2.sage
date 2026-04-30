# based on https://github.com/Neobeo/HackTM2023/blob/main/solve420.sage and https://github.com/y011d4/my-ctf-challenges/blob/main/2023-HackTMCTF-2023/crypto/glp-420/sol/solve.sage
# obviously unintended :)
from sage.all import *
from util import sample_poly, encode_m
from hashlib import sha256
from subprocess import check_output
from re import findall
from time import time
from binteger import Bin
from helper import *

seed = sha256(b"welcome to D3CTF").digest() + sha256(b"have a nice day").digest()
Af = sample_poly(seed, 0, 2**32 - 5).f
# fmt: off
Bf = b
# fmt: on

q = 2**32 - 5
n = 512
F = GF(q)["x"]
a = F(Af)
b = F(Bf)


x = F.gen()
ps = [
    x - 1,
    x + 1,
    x**2 + 1,
    x**4 + 1,
    x**8 + 1,
    x**16 + 1,
    x**32 + 1,
    x**64 + 1,
    x**128 + 1,
    x**256 + 1,  # too big for LLL/flatter to solve svp
]
# this must hold over Z[x] instead of Zq[x]
assert prod(ps) == x**n - 1


def flatter(M):
    # compile https://github.com/keeganryan/flatter and put it in $PATH
    z = "[[" + "]\n[".join(" ".join(map(str, row)) for row in M) + "]]"
    ret = check_output(["flatter"], input=z.encode())
    return matrix(M.nrows(), M.ncols(), map(int, findall(b"-?\\d+", ret)))


def solve(poly, a, b, slen=None):
    # solve for a*s+e=b (mod poly)
    # where s and e are small
    # and len(s) = slen
    global mat, mat2
    n = poly.degree()
    if slen is None:
        slen = n
    print(f"Try solving with deg(poly) = {n}")
    t0 = time()
    main_block = matrix([vector(a * x**i % poly) for i in range(n)])
    approx = 512 // n  # approximation for the average of target vector
    mat = block_matrix(
        ZZ,
        [
            [1, -main_block, 0],
            [0, q, 0],
            # kannan embedding
            [
                0,
                matrix(vector(b % poly)),
                matrix([[approx]]),
            ],
        ],
    )
    mat[:, slen:n] *= q  # force zero
    print(f"Lattice size = {mat.dimensions()}")
    mat2 = flatter(mat)
    print(f"{mat.nrows()}x{mat.ncols()} lattice reduced in {time()-t0}")
    for ret in mat2:
        if ret[-1] < 0:
            ret = -ret
        if ret[-1] == approx:
            print(ret)
            print()
            return F(list(ret[:n]))


rs = [solve(p, a, b) for p in ps[:-1]]
L = lcm(ps[:-1])  # deg(L) = 256
s_mod_L = crt(rs, ps[:-1])  # this is s (mod L)
e_mod_L = (b - a * s_mod_L) % L
print(s_mod_L)
print(e_mod_L)

# use known information to simplify the problem
ks = F(encode_m(b"antd3ctf{" + b"\x00" * (64 - 9 - 1) + b"}").f)
l = 8 * 9
# a(ks+s'*x^l)+e = b
# a*x^l*s'+e=b-a*ks
# deg(s') = 8*(64-9-1) = 432
ap = (a * x**l) % (x**n - 1)
bp = (b - a * ks) % (x**n - 1)
sp_mod_L = (s_mod_L - ks) * inverse_mod(x**l, L) % L

# a'*(sp_mod_L+L*u)+e=b'
# a'*L*u+e=b'-a'*sp_mod_L
rem = ps[-1]
app = ap * L % rem
bpp = (bp - ap * sp_mod_L) % rem
# uu = u (mod rem)
# but since deg(u) = 512-8*(9+1)-256, uu = u
uu = solve(rem, app, bpp, slen=512 - 8 * (9 + 1) - 256)  # ~10min

print(Bin(list((sp_mod_L + L * uu) * x**l + ks)).bytes)
# antd3ctf{Dual^attack_1s_real1y_inteRest1ng!@#$L@tT1ce_MaSter!!!}