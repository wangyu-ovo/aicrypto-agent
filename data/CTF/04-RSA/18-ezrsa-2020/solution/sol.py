from Crypto.Util.number import *
import gmpy2
from helper import *

e = 54722
print(len(bin(gift)[2:]))
print(len(bin(n)[2:]))

# gift * gcd = (p-1) * (q-1)
# gift % gcd = 0
for gcd_val in range(4, 8):
    phi = gift * gcd_val
    try:
        d = gmpy2.invert(e // 2, phi)
        m_2 = pow(c, int(d), n)
        flag = long_to_bytes(gmpy2.isqrt(m_2))
        print(flag)
    except ZeroDivisionError:
        continue
