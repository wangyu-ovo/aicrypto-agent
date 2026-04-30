from Crypto.Util.number import *
from gmpy2 import *
from helper import *


n = N
beta = 0.34
delta = 0.02
amplification = 2048
X = int(pow(n,delta) * (5/2))
Y = int(pow(n,(beta+delta)) * (5/2))
M = []
M.append([n*n*X*X*X,0,0,0])
M.append([e*n*X*X*X,-n*X*X*Y,0,0])
M.append([e*e*X*X*X,-2*e*X*X*Y,X*Y*Y,0])
M.append([e*e*e*X*X*X,-3*e*e*X*X*Y,3*e*X*Y*Y,-Y*Y*Y])
M = Matrix(M)
A = M.LLL()[0]
p = []
p.append(A[0]//(X**3))
p.append(A[1]//(X^2*Y))
p.append(A[2]//(X*Y^2))
p.append(A[3]//(Y^3))
R.<x,y> = ZZ[]
f = x**3*p[0] + x**2*y*p[1] + x*y**2*p[2] + y**3*p[3]
ffl = f.factor()

k = ffl[0][0].coefficients()[0] + 1
dq = ffl[0][0].coefficients()[1]
q = (e * dq + k - 1) // k
p = n // q
assert n == p * q
phi = (p-1) * (q-1)
d = inverse(e,phi)
m = pow(c,d,n)
flag = long_to_bytes(m)
print(flag)
