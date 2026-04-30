import contextlib
import itertools
from helper import *

from Crypto.Util.number import long_to_bytes
# from sage.all_cmdline import Integer, inverse_mod, x

m = 19
poly = sum(e * x ** i for i, e in enumerate(Integer(n).digits(m)))
(p, _), (q, _), (r, _) = poly.factor_list()
p, q, r = p(x=m), q(x=m), r(x=m)

assert p * q * r == n

for z in itertools.count(10):
    with contextlib.suppress(ZeroDivisionError, UnicodeDecodeError):
        e = m ** 3 + z - 2
        d = inverse_mod(e, (p - 1) * (q - 1) * (r - 1))
        print(long_to_bytes(pow(c, int(d), n)).decode())
        break
