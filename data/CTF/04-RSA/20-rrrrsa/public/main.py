import hashlib
import sympy
from Crypto.Util.number import *

flag = 'GWHT{************}'

flag1 = flag[:19].encode()
flag2 = flag[19:].encode()
assert(len(flag) == 38)

P1 = getPrime(1038)
P2 = sympy.nextprime(P1)
assert(P2 - P1 < 1000)

Q1 = getPrime(512)
Q2 = sympy.nextprime(Q1)

N1 = P1 * P1 * Q1
N2 = P2 * P2 * Q2

E1 = getPrime(1024)
E2 = sympy.nextprime(E1)

m1 = bytes_to_long(flag1)
m2 = bytes_to_long(flag2)

c1 = pow(m1, E1, N1)
c2 = pow(m2, E2, N2)


output = open('secret', 'w')
output.write('N1=' + str(N1) + '\n')
output.write('c1=' + str(c1) + '\n')
output.write('E1=' + str(E1) + '\n')
output.write('N2=' + str(N2) + '\n')
output.write('c2=' + str(c2) + '\n')
output.write('E2=' + str(E2) + '\n')
output.close()
