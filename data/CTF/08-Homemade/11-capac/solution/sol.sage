from Crypto.Util.number import *
import itertools
load('helper.sage')

# use yafu
p = 242195390295637766135570468161415180323
q = 171955359080932502551172606124599656543
o = p^3 * q^5 * (p^2+p+1)*(q^2+q+1)*(p-1)*(q-1)
n = p^4 * q^6
n_, e = pubkey
assert n == n_

def add(P, Q, c, n):
	# Add two points P and Q on curve x^3 + c*y^3 + c^2*z^3 - 3*c*x*y*z = 1 in Zmod(n) 
	(x1, y1, z1) = P
	(x2, y2, z2) = Q
	x3 = (x1*x2 + c*(y2*z1	+ y1*z2))	% n
	y3 = (x2*y1 + x1*y2		+ c*z1*z2)	% n
	z3 = (y1*y2 + x2*z1		+ x1*z2)	% n
	return (x3, y3, z3)


def mul(P, g, c, n):
	# Scalar multiplication on curve
	(x1, y1, z1) = P
	(x2, y2, z2) = (1, 0, 0)
	for b in bin(g)[2:]:
		(x2, y2, z2) = add((x2, y2, z2), (x2, y2, z2), c, n)
		if b == '1': 
			(x2, y2, z2) = add((x2, y2, z2), (x1, y1, z1), c, n)
	return (x2, y2, z2)

def lift(f, p, k, previous):
    result = []
    df = diff(f)
    for lower_solution in previous:
        dfr = Integer(df(lower_solution))
        fr = Integer(f(lower_solution))
        if dfr % p != 0:
            t = ZZ((-(xgcd(dfr, p)[1]) * int(fr // p ** (k - 1))) % p)
            x_ = lower_solution + t * p ** (k - 1)
            result.append(x_)
        if dfr % p == 0:
            if fr % p ** k == 0:
                for t in range(0, p):
                    x_ = lower_solution + t * p ** (k - 1)
                    result.append(x_)
    return result

def hensel_lifting(f, p, k, base_solution):
    solution = base_solution
    for i in range(2, k + 1):
        solution = lift(f, p, i, solution)
    return solution


def get_c(P, p, k):
    x, y, z = P
    PR.<c> = PolynomialRing(Zmod(p))
    f = x^3 + c*y^3 + c^2*z^3 - 3*c*x*y*z - 1
    c_list = [ZZ(x) for x, rep in f.roots()]
    
    PR.<c> = PolynomialRing(Zmod(p^k))
    f = x^3 + c*y^3 + c^2*z^3 - 3*c*x*y*z - 1
    c_list = hensel_lifting(f, p, k, c_list)
    c = ZZ(c_list[0])
    return c_list

cp_list = get_c(enc, p, 4)
cq_list = get_c(enc, q, 6)

d = inverse_mod(e, o)
for cp, cq in itertools.product(cp_list, cq_list):
    c = crt([ZZ(cp), ZZ(cq)], [p^4, q^6])
    m = mul(enc, d, c, n)
    x, y, z = m
    msg = long_to_bytes(int(m[0])) + long_to_bytes(int(m[1]))
    print(msg)