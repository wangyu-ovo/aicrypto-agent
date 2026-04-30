from sage.all import *
from helper import *
from Crypto.Util.number import *


factor_l = factor(N)
p = factor_l[0][0]
q = factor_l[1][0]
d = inverse(e,(p-1)*(q-1))
print(long_to_bytes(pow(c,d,N)))
