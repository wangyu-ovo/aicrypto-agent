from sage.all import GF, Matrix, vector
from Crypto.Util.number import long_to_bytes
from helper import *

"""
m * Q[0] + r0 * R[0] + s0 * S[0] = C[0]
m + r0 * R[0] * Q[0]^-1 + s0 * S[0] * Q[0]^-1 = C[0] * Q[0]^-1
m + r1 * R[1] * Q[1]^-1 + s1 * S[1] * Q[1]^-1 = C[1] * Q[1]^-1
r0 * R[0] * Q[0]^-1 + s0 * S[0] * Q[0]^-1 - r1 * R[1] * Q[1]^-1 - s1 * S[1] * Q[1]^-1 = C[0] * Q[0]^-1 - C[1] * Q[1]^-1
"""
Q = vector(GF(p), Q)
A = Matrix([
  [1, 0, 0, 0, 0, int(R[0] * Q[0] ** -1)],
  [0, 1, 0, 0, 0, int(S[0] * Q[0] ** -1)],
  [0, 0, 1, 0, 0, int(R[1] * Q[1] ** -1)],
  [0, 0, 0, 1, 0, int(S[1] * Q[1] ** -1)],
  [0, 0, 0, 0, 1, -p],
  [0, 0, 0, 0, 0, int(C[0] * Q[0] ** -1 - C[1] * Q[1] ** -1)],
])

print(A.LLL()[0])
# (-2638621544, -3219364802, 3791125439, 2479984130, -136018362, 0)

r1 = 3791125439
s1 = 2479984130
m = (C[1] - s1 * S[1] - r1 * R[1]) * Q[1] ** -1
print(long_to_bytes(int(m)).decode())
