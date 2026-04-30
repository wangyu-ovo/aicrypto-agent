#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def u(a, x, y):
    assert a.is_integer() and x.is_rational() and y.is_rational()
    return x + Rational((a * x - y)/(x ** 2 + y ** 2))

def v(a, x, y):
    assert a.is_integer() and x.is_rational() and y.is_rational()
    return y - Rational((x + a * y)/(x ** 2 + y ** 2))

m1 = Integer(bytes_to_long(flag[:len(flag)//2]))
m2 = Integer(bytes_to_long(flag[len(flag)//2:]))
a = Integer(randint(1, 1 << 512))

print(f'A = {u(5, a, 4*a)}')
print(f'U = {u(a, m1, m2)}')
print(f'V = {v(a, m1, m2)}')