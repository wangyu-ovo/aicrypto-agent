import re
from Crypto.Util.number import bytes_to_long


with open("./output.txt") as fp:
    for _ in range(2):
        _ = fp.readline()
    c_m1_list = list(map(int, re.findall(r"c1 = (\d+) \+ (\d+)\*i \+ (\d+)\*j \+ (\d+)\*k", fp.readline().strip())[0]))
    c_m2_list = list(map(int, re.findall(r"c2 = (\d+) \+ (\d+)\*i \+ (\d+)\*j \+ (\d+)\*k", fp.readline().strip())[0]))

m1 = bytes_to_long(b"I have implemented Paillier 4.0. Can you break it?")
n = gcd(c_m1_list[1:])
for prime in prime_range(10000):
    while n % prime == 0:
        n //= prime

Q = QuaternionAlgebra(Zmod(n**2), -1, -1)
c1 = Q(c_m1_list)
c2 = Q(c_m2_list)