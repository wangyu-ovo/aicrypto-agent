import re, os
from Crypto.Util.number import bytes_to_long, long_to_bytes

load('./helper.sage')
m1 = bytes_to_long(b"I have implemented Paillier 4.0. Can you break it?")
n = gcd(c_m1_list[1:])
for prime in prime_range(10000):
    while n % prime == 0:
        n //= prime

Q = QuaternionAlgebra(Zmod(n**2), -1, -1)
i, j, k = Q.gens()
tmp = c1 ** pow(m1, -1, n)
g_ = tmp * pow(tmp[0], -1, n)  # g_ == g mod n
mk = (int(c2[1]) // n) * pow(int(g_[1]) // n, -1, n**2) % n
k = (c2[0] - (g_[0] - 1) * mk) % n
m = mk * pow(k, -1, n) % n

print(long_to_bytes(int(m)))