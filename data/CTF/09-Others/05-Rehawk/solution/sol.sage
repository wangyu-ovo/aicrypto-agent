m = 128
C = CyclotomicField(m)
F, PHI = C.maximal_totally_real_subfield()
zeta1280 = F.gen()
load('./helper.sage')
PR = PolynomialRing(F, ["a", "b", "c", "d"])
a, b, c, d = PR.gens()
sk_sym = matrix([[a, c], [b, d]])
eqs = (
    (sk_sym + identity_matrix(2)) * (sk_sym.T - identity_matrix(2)) - pkey
).list() + [a * d - b * c - 1]
I = ideal(eqs)
V = I.variety()
sol = V[0]
a, b, c, d = sol[a], sol[b], sol[c], sol[d]
sk = Matrix([[a, c], [b, d]])

from hashlib import sha256
flag = str(sum(sk.coefficients()).polynomial()(2^128))
flag = 'CCTF{' + sha256(flag.encode()).hexdigest() + '}'
print(f'{flag = }')