# solve for p
from helper import *
F.<p> = ZZ[]
f = p * (p + 6) * (p + 12) - n
print(f.roots())
p = int(f.roots()[0][0])

from Crypto.Util.number import long_to_bytes
q = p + 6
r = p + 12

phi = (p-1) * (q-1) * (r-1)
d = pow(e,-1,phi)

flag = long_to_bytes(pow(ct,d,n))
print(flag)
