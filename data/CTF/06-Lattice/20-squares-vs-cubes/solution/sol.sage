from Crypto.Util.number import *
from helper import *


def polypow(base, exp, mod):
    return (mod.parent().quo(mod)(base) ** exp).lift()

𝜁 = polygen(Zmod(N))
p = gcd(N, ZZ((polypow(𝜁**3 - m1, N, 𝜁**2 - m0) + x0 - x1).monic()[0]**2 - m0))
print(f'{p = }')

qrf = ZZ(-(polypow(𝜁**3 + p**3 - m1, N, 𝜁**2 + p**2 - m0) + x0 - x1).monic()[0])
print(f'{qrf = }')

qr = N//p
q_approx = bytes_to_long(b'SEKAI{' + bytes(122)) * qr // qrf
print(f'{q_approx = }')

y = Zmod(qr)['y'].gen()
q = ZZ((y*(y-qrf))(y=y+q_approx).small_roots(X = 2**464, epsilon=0.08)[0]) + q_approx
print(f'{q = }')

print(long_to_bytes(qrf * q // qr))