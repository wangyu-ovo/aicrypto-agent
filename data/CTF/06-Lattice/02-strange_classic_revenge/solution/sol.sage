from hashlib import sha1
from helper import *


Bits = 16
m = 32
K = 2


def get_orthogonal_basis(B):
    M = block_matrix(ZZ, [B, identity_matrix(B.nrows())], ncols=2)
    return M.LLL()[:m//2, -m:]


sub_lattice = []
for i in range(len(cipher)):
    mix0, mix1 = cipher[i]
    my_A0k = get_orthogonal_basis(Matrix(mix0).transpose())
    my_A1k = get_orthogonal_basis(Matrix(mix1).transpose())
    sub_lattice.append(block_matrix([Matrix(my_A0k.right_kernel().basis()), Matrix(my_A1k.right_kernel().basis())], nrows=2))

L2 = block_matrix(ZZ, sub_lattice, nrows=K)
print('MRCTF{%s}' % sha1(str(L2.hermite_form()[:m]).encode()).hexdigest())