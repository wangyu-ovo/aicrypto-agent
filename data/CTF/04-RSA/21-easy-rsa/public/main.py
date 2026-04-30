from random import randint
from gmpy2 import *
from Crypto.Util.number import *

def getprime(bits):
    while 1:
        n = 1
        while n.bit_length() < bits:
            n *= next_prime(randint(1,1000))
        if isPrime(n - 1):
            return n - 1

m = bytes_to_long(b'flag{************************************}')

p = getprime(505)
q = getPrime(512)
r = getPrime(512)
assert m < q

n = p * q * r
e = 0x10001
d = invert(q ** 2, p ** 2)
c = pow(m, 2, r)
cipher = pow(c, e, n)

print(n)
print(d)
print(cipher)


