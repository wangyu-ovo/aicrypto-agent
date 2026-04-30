from Crypto.Util.number import *
from secret import secret, flag
def encrypt(m):
    return pow(m, e, n)
assert flag == b"dasctf{" + secret + b"}"
e = 11
p = getPrime(512)
q = getPrime(512)
n = p * q
P = getPrime(512)
Q = getPrime(512)
N = P * Q
gift = P ^ (Q >> 16)
print(N, gift, pow(n, e, N))
print(encrypt(bytes_to_long(secret)),
    encrypt(bytes_to_long(flag)))