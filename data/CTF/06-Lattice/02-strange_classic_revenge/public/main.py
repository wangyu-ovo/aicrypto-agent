from sage.all import *
from secret import flag
from hashlib import sha1


Bits = 16
m = 32
K = 2
while True:
    L0 = random_matrix(ZZ, m, x=0, y=2**Bits)
    if is_prime(L0.det()):
        break


def Rotor(x):
    return (vector(x) * random_matrix(ZZ, m, x=0, y=2**Bits) * L0).change_ring(ZZ).list()


def get_mixed(A):
    mix = []
    for j in range(len(A)):
        for jj in range(j + 1, len(A)):
            w = [getrandbits(200) for _ in range(len(A))]
            mix.append(vector([int(sqrt(abs(A[j][ii] * A[jj][ii]))) + vector(w) * vector([A[jjj][ii] for jjj in range(len(A))]) for ii in range(len(A[0]))]))
    return mix[:m//2]


vectors = [Rotor(random_vector(ZZ, m, x=0, y=2**Bits).list()) for _ in range(m+K)]
cipher = []
for i in range(K):
    mix0 = get_mixed(vectors[i:i+m//2])
    mix1 = get_mixed(vectors[i+m//2:i+m])
    cipher.append([mix0, mix1])
print('cipher =', cipher)
assert flag.lstrip('MRCTF{').rstrip('}') == sha1(str(L0.hermite_form()).encode()).hexdigest()