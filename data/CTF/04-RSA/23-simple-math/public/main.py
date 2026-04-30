from Crypto.Util.number import getPrime
import hashlib

e = 2022
m = getPrime(512)
m1 = getPrime(512)
m2 = getPrime(512)
flag = m + m1 + m2
flag = hashlib.md5(str(flag).encode('utf-8')).hexdigest()

c1 = pow(m + m1, e, m * m1)
c2 = pow(m + m2, e, m * m2)
c3 = pow(m1 + m2, e, m1 * m2)

x = pow(m1 + 2022, m, m * m1)
y = pow(m2 + 2022, m, m * m2)
z = pow(m + 2022, m1, m * m1)

print('c1 =', c1)
print('c2 =', c2)
print('c3 =', c3)
print('x =', x)
print('y =', y)
print('z =', z)

