from gmpy2 import *
from random import *
from Crypto.Util.number import *
from os import urandom
from flag import flag

P_bits = 444
Q_bits = 666
R_bits = 333
key_num = 9
e = 0x1337

while True:
    could_not_solve = False
    p = getPrime(P_bits)
    if gcd(p-1, e) != 1:
        continue
    R = []
    Q = []
    N = []
    for i in range(key_num):
        Q.append(getPrime(Q_bits))
        R.append(getrandbits(R_bits))
        N.append(p * Q[-1] + R[-1])
        if gcd(Q[-1], e) != 1:
            could_not_solve = True
            break
    if not could_not_solve:
        break


C = []
assert len(flag) == 45
for i in range(key_num):
    tmp_cipher = flag[i*len(flag)//key_num:(i+1)*len(flag)//key_num].encode()
    tmp_cipher = urandom(128 - len(tmp_cipher)) + tmp_cipher
    tmp_cipher = pow(bytes_to_long(tmp_cipher), e, p * Q[i])
    C.append(tmp_cipher)

print('N =', N)
print('C =', C)

'''
'''