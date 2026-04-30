from hashlib import sha256

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
# from pwn import remote
load('./helper.sage')

nonce = bytes.fromhex(nonce)
enc = bytes.fromhex(enc)


def hash_Q(x):
    return sha256(
        long_to_bytes(int(x[0]))
        + long_to_bytes(int(x[1]))
        + long_to_bytes(int(x[2]))
        + long_to_bytes(int(x[3]))
    ).digest()


def matmul(A, B):
    res = []
    for i in range(4):
        row = []
        for j in range(4):
            tmp = 0
            for k in range(4):
                tmp += A[i][k] * B[k][j]
            row.append(tmp)
        res.append(row)
    return res


def solve(ShareA, PubA, PubB):
    PR = PolynomialRing(Zmod(p), names=[f"a{i}{j}" for i in range(4) for j in range(4)])
    a_list = PR.gens()
    Amat = [[a_list[4*i+j] for j in range(4)] for i in range(4)]
    lhs = matmul(PubB, Amat)
    rhs = matmul(Amat, ShareA)
    polys = []
    for i in range(4):
        for j in range(4):
            polys.append(lhs[i][j] - rhs[i][j])
    for i in range(3):
        polys.append(Amat[0][0] - Amat[i+1][i+1])
    polys.append(Amat[0][1] + Amat[1][0])
    polys.append(Amat[0][1] + Amat[2][3])
    polys.append(Amat[0][1] - Amat[3][2])
    polys.append(Amat[0][2] - Amat[1][3])
    polys.append(Amat[0][2] + Amat[2][0])
    polys.append(Amat[0][2] + Amat[3][1])
    polys.append(Amat[0][3] + Amat[1][2])
    polys.append(Amat[0][3] - Amat[2][1])
    polys.append(Amat[0][3] + Amat[3][0])
    mat = matrix(Zmod(p), len(polys), 16)
    vec = vector(Zmod(p), len(polys))
    for i in range(len(polys)):
        for j, a in enumerate(a_list):
            term = {_a: 1 if _a == a else 0 for _a in a_list}
            mat[i, j] = polys[i].coefficient(term)
            vec[i] = -polys[i].constant_coefficient()
    K = mat.right_kernel_matrix()

    mat = matrix(Zmod(p), 3, 3)
    mat[0] = K[0, 1:4]
    mat[1] = K[1, 1:4]
    mat[2, 0] = PubA[0, 1]
    mat[2, 1] = PubA[0, 2]
    mat[2, 2] = PubA[0, 3]
    vec = vector(Zmod(p), 3)
    tmp = mat.left_kernel_matrix()[0]
    tmp_K = tmp[:2] * K

    i, j, k = Q.gens()
    _A = tmp_K[0] + tmp_K[1] * i + tmp_K[2] * j + tmp_K[3] * k
    return _A


ShareA = share_A.matrix()
ShareB = share_B.matrix()
PubA = pub_A.matrix()
PubB = pub_B.matrix()
_A = solve(ShareA, PubA, PubB)
_B = solve(ShareB, PubB, PubA)
K = _A**-1 * _B**-1 * _A * _B

key = hash_Q(K)
cipher = AES.new(key, mode=AES.MODE_CTR, nonce=nonce)
flag = cipher.decrypt(enc)
print(flag)
