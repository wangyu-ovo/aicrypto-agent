import itertools
from Crypto.Cipher import AES
from Crypto.Util.number import *
from hashlib import sha256

def check(l):
    return sum([i>=10 and i<=1000 for i in l]) == 320 or sum([-i>=10 and -i<=1000 for i in l]) == 320

def get_A(res, idx_list, op_list):
    A_cols = []
    for a, b, c, d, e in idx_list:
        for op in op_list:
            v = res[a]*op[0] + res[b]*op[1] + res[c]*op[2] + res[d]*op[3] + res[e]*op[4]
            if check(v) and (v not in A_cols) and (-v not in A_cols):
                A_cols.append(v)
            if len(A_cols) == 5:
                return A_cols

def get_s(A, b):
    basis = A.transpose().change_ring(ZZ).stack(1000 * identity_matrix(64)).hermite_form()[:64]
    res = block_matrix([[matrix(ZZ, 1, 1, [3]), matrix(b)], [matrix(ZZ, 64, 1, [0] * 64), basis]])
    res = res.LLL(beta = 25)
    e = res[0][1:]
    try:
        s = A.solve_right(b - e)
        return s
    except:
        return None


from helper import *
B = Matrix(ZZ, 7, 320, B_list)
J = Matrix(ZZ, 64, 25, M_list)
R = Matrix(ZZ, 65, 1, R_list)

iv = long_to_bytes(int(output, 16))[:16]
ct = long_to_bytes(int(output, 16))[16:]

res = B.LLL()
idx_list = list(cartesian_product([[2, 3, 4, 5, 6] for _ in range(5)]))
op_list = list(cartesian_product([[-1, 0, 1] for _ in range(5)]))
ans = get_A(res, idx_list, op_list)
ans = [i if i>0 else -i for i in ans]
possible_A  = list(map(Matrix, list(itertools.permutations(ans))))
possible_A  = [i.transpose() for i in possible_A]

T = R[:-1].transpose()
V = R[-1]
k = T.transpose().stack(V).transpose()
kk = k.right_kernel_matrix()
kkk = kk.LLL()
b = kkk[0][:-1]

for A in possible_A:
    try:
        AA = Matrix(Zmod(1000), 64, 25, [int(i).__xor__(int(j)) for i,j in zip(A.list(), J.list())])
        res = get_s(AA, b)
        key = sha256(''.join(list(map(str, res))).encode()).digest()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        if pt.startswith(b"flag{"):
            print(pt)
            break
    except:
        continue
