from Crypto.Util.number import *
from helper import *
d = len(str(enc))

enc = (enc - pkey) % (10 ** d)
m = (pow(d, -2, 10 ** d) * enc) % (10 ** d)

print(long_to_bytes(int(str(m).rstrip('1'))))
