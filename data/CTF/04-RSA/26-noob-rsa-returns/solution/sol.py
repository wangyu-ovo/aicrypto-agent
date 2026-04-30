import math
import binascii
from helper import *


C = 0xbaaaaaad
D = 0xdeadbeef
A = 0xbaadf00d

p = math.gcd(pow(2, A - C + D, n) - pow(2, e * K, n), n)
q = n // p

d = pow(e, -1, (p - 1) * (q - 1))

print(binascii.unhexlify(hex(pow(ct, d, n))[2:]))

# Flag: BITSCTF{I_H0P3_Y0UR3_H4V1NG_FUN_S0_F4R_EHEHEHEHEHO_93A5B675}
