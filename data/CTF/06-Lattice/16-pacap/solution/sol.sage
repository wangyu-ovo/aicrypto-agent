from lll_cvp import polynomials_to_matrix, flatter
from Crypto.Util.number import long_to_bytes
import itertools
load('helper.sage')

n, e = pubkey
cx, cy, cz = enc
sz = 2 ** (8 * l // 2)

PR = PolynomialRing(ZZ, ["x", "y"])
x, y = PR.gens()


# Res(cx ^ 3 + c * cy ^ 3 + c ^ 2 * cz ^ 3 - 3 * c * cx * cy * cz - 1, x ^ 3 + c * y ^ 3 - 1, c)
# = y^6 * cx^3 + y^3 * (1 - x^3) * cy^3 + (1 - x^3)^2 * cz^3 - 3 * y^3 * (1 - x^3) * cx * cy * cz - y^6
# we can simplify it by letting u = 1 - x^3 and v = y^3

PR = PolynomialRing(ZZ, ["u", "v"])
u, v = PR.gens()
f = v**2 * cx**3 + v * u * cy**3 + u**2 * cz**3 - 3 * v * u * cx * cy * cz - v**2


def small_polys(f, bounds, m=1, d=None):
    if d is None:
        d = f.degree()

    R = f.base_ring()
    N = R.cardinality()
    f_ = (f // f.lc()).change_ring(ZZ)
    f = f.change_ring(ZZ)
    l = f.lm()

    M = []
    for k in range(m + 1):
        M_k = set()
        T = set((f ^ (m - k)).monomials())
        for mon in (f ^ m).monomials():
            if mon // l ^ k in T:
                for extra in itertools.product(range(d), repeat=f.nvariables()):
                    g = mon * prod(map(power, f.variables(), extra))
                    M_k.add(g)
        M.append(M_k)
    M.append(set())

    shifts = Sequence([], f.parent())
    for k in range(m + 1):
        for mon in M[k] - M[k + 1]:
            g = mon // l ^ k * f_ ^ k * N ^ (m - k)
            shifts.append(g)

    B, monomials = polynomials_to_matrix(shifts)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    # B = flatter(B)
    B = B.LLL()

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)
    B = B.change_ring(ZZ)
    H = Sequence([h for h in B * monomials if not h.is_zero()])
    return H


H = small_polys(f.change_ring(Zmod(n)), (sz**3, sz**3), m=5)
h = H[0].gcd(H[1])  # a*u+b*v
c = -h.coefficients()[1] / h.coefficients()[0] % n
assert (cx ^ 3 + c * cy ^ 3 + c ^ 2 * cz ^ 3 - 3 * c * cx * cy * cz - 1) % n == 0, "???"

# a*u+b*v=0
# a*(1-x^3)+b*y^3=0
# y^3=k*a for some k=gcd(1-x^3,y^3)

for k in range(1, 100):
    try:
        y = (k * h).coefficients()[0].nth_root(3)
        uval = h.subs(v=y ^ 3).univariate_polynomial().roots(multiplicities=False)[0]
        x = (1 - uval).nth_root(3)
        print(long_to_bytes(int(x)) + long_to_bytes(int(y)))
        break
    except:
        pass
