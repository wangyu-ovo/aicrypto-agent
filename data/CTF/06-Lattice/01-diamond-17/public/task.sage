#!/usr/bin/env sage
import os
from hashlib import sha256
from Crypto.Cipher import AES
from sage.crypto.lwe import LWE
from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler as DGDIS


FLAG = b'*********' # to decrypt, The number of * does not represent the length of the plaintext

A = random_matrix(ZZ, 320, 5, x=10, y=1000)
B = Matrix(A * vector([randint(1, 2 ^ 1024) for _ in range(5)]) for _ in range(7))

L = LWE(n=25, q=1000, D=DGDIS(3))
S = [L() for _ in range(64)]

M = Matrix(64, 25, [int(i).__xor__(int(j)) for i, j in zip(A.list(), (Matrix([x for x, _ in S])).list())])
T = Matrix([randint(1, 2 ^ 1024) for _ in range(64)])
R = T.transpose().stack(T * vector([y for _, y in S]).change_ring(ZZ))

if __name__ == "__main__":
    key = sha256(''.join(list(map(str, L._LWE__s))).encode()).digest()
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(FLAG)

    f = open("data/data/Lattice/diamond/challenge/output.txt", "wb")
    blist_file = open("data/data/Lattice/diamond/challenge/B_list.txt", "wb")
    mlist_file = open("data/data/Lattice/diamond/challenge/M_list.txt", "wb")
    rlist_file = open("data/data/Lattice/diamond/challenge/R_list.txt", "wb")

    f.write((iv + ct).hex().encode())
    blist_file.write(str(B.list()).encode() + b'\n')
    mlist_file.write(str(M.list()).encode() + b'\n')
    rlist_file.write(str(R.list()).encode() + b'\n')
    
    
    f.close()
