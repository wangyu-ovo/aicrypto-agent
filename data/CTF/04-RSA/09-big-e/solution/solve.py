from Crypto.Util.number import bytes_to_long, long_to_bytes
from helper import *
inv1 = pow(e_1, -1, e_2)
inv2 = e_1*inv1 // e_2
assert e_1*inv1 - e_2*inv2 == 1

pt = (pow(ct_1, inv1, n) * pow(pow(ct_2, inv2, n), -1, n)) % n
print(long_to_bytes(pt))
