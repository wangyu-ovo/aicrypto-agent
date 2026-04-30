from Crypto.Util.number import *
from gmpy2 import gcd
import hashlib
from helper import *

e = 2022

k1m = (pow(x - 2022, e) - pow(y - 2022, e)) - (c1 - c2)
k2m = (pow(x - 2022, e) + pow(y - 2022, e)) - (c1 + c2)
m = gcd(k1m, k2m)
assert isPrime(m)

m1m = x % m - 2022
m2m = y % m - 2022

for i in range(10):
    m1 = m1m + i * m
    if pow(m + m1, e, m * m1) == c1:
        print('got')
        break

for i in range(10):
    m2 = m2m + i * m
    if pow(m + m2, e, m * m2) == c2:
        print('got')
        break

assert pow(m + 2022, m1, m * m1) == z
print(hashlib.md5(str(m + m1 + m2).encode('utf-8')).hexdigest())
