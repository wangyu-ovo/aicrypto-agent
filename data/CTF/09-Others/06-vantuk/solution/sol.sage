import contextlib

from Crypto.Util.number import long_to_bytes
from sage.all import Integer, Rational, assume, solve, var

def u(a, x, y):
    assert a.is_integer() and x.is_rational() and y.is_rational()
    return x + Rational((a * x - y)/(x ** 2 + y ** 2))

def v(a, x, y):
    assert a.is_integer() and x.is_rational() and y.is_rational()
    return y - Rational((x + a * y)/(x ** 2 + y ** 2))

load('./helper.sage')
a = Integer(A.denominator() / 17)
assert A == u(Integer(5), a, 4 * a)

x, y = var("x, y")
assume([x > 0, y > 0])
sol = solve([
    U.denominator() * (x * (x ** 2 + y ** 2 + a) - y) == U.numerator() * (x ** 2 + y ** 2),
    V.denominator() * (y * (x ** 2 + y ** 2 - a) - x) == V.numerator() * (x ** 2 + y ** 2),
], x, y)

for x0, y0 in sol:
    # RuntimeError: no explicit roots found
    # TypeError: Unable to coerce x0 to an integer
    with contextlib.suppress(RuntimeError, TypeError):
        x0, y0 = Integer(x0.roots()[0][0]), Integer(y0.roots()[0][0])
        assert U == u(a, x0, y0)
        assert V == v(a, x0, y0)
        print((long_to_bytes(x0) + long_to_bytes(y0)).decode())
