import numpy as np
from Crypto.Util.number import inverse, long_to_bytes
from helper import *

d = 563  # len(h.digits()) // 2
q = 4 * 100 ** d

v1 = np.array((1, h))
v2 = np.array((0, q))

def gauss(v1, v2):
    while True:
        if v1.dot(v1) > v2.dot(v2):
            v1, v2 = v2, v1
        m = v1.dot(v2) // v1.dot(v1)
        if m == 0:
            return v1, v2
        v2 = v2 - m * v1


def decrypt(c, f, g, q):
    return (c * f % q) * inverse(f, f + g) % (f + g)

    # a = (f * e) % q
    # m = (a * inverse(f, (f + g))) % (f + g)
    # return m

(f, g), _ = gauss(v1, v2)
print(long_to_bytes(decrypt(c, f, g, q)).decode())
