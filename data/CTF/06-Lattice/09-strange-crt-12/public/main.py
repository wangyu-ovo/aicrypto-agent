from gmpy2 import *
from random import *
from Crypto.Util.number import *
from flag import flag


beta = 0.34
delta = 0.02
amplification = 2048

p = getPrime(int(beta * amplification))
q = getPrime(int((1 - beta) * amplification))
N = p * q

while True:
    dq = getrandbits(int(delta*amplification))
    dp = getrandbits(int((beta-delta) * amplification))
    if (dp-dq) % gcd(p-1, q-1) != 0:
        continue
    d = ((inverse((p-1)//gcd(p-1, q-1), (q-1)//gcd(p-1, q-1)) * (dq-dp)//gcd(p-1, q-1)) % ((q-1)//gcd(p-1, q-1))) * (p-1) + dp
    if gcd(d, (p-1)*(q-1)) == 1:
        break

e = inverse(d, (p-1)*(q-1))
m = bytes_to_long(flag.encode())
c = pow(m, e, N)
print('N =', N)
print('e =', e)
print('c =', c)

