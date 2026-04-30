from util import *
from hashlib import *
import os
# from secret import flag
from Crypto.Util.number import *

assert flag[:9] == b'antd3ctf{' and flag[-1:] == b'}' and len(flag) == 64
assert sha256(flag).hexdigest() == '8ea9f4a9de94cda7a545ae8e7c7c96577c2e640b86efe1ed738ecbb5159ed327'

flag = b'a' * 16 + b'b' * 16 + b'2' * 32
seed = sha256(b"welcome to D3CTF").digest() + sha256(b"have a nice day").digest()
A = sample_poly(seed , 0 , 2**32 - 5)
e = sample_poly(os.urandom(64) , -4 , 4)
s = encode_m(flag)
b = A*s + e
print(b.f)
