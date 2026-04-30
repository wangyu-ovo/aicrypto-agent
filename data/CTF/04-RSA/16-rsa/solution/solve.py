from sympy import root
from Crypto.Util.number import long_to_bytes
from helper import *

m = int(root(c, e))
flag = long_to_bytes(m)
print(f"Flag: {flag.decode()}")
