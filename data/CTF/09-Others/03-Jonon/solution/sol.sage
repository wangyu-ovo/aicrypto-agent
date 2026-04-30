from copy import deepcopy

load("./helper.sage")
nbit = 256
k, l, _B = 5, 19, 63
M, As, Ep = mat_list[:l], mat_list[l:2*l], mat_list[-1]

def gao_one(i):
    Mi, Asi = M[i], As[i]
    wtf = Asi^-1 * Ep^-1 * Mi * Ep
    a = wtf[0, 0]
    return a

plist = []
for i in range(1, l):
    pi = gao_one(0) - gao_one(i)
    plist.append(pi.numerator())
p = gcd(plist)
Zp = Zmod(p)
M = [A.change_ring(Zp) for A in M]
As = [A.change_ring(Zp) for A in As]
Ep = Ep.change_ring(Zp)
Ds = As[0]^-1 * Ep^-1 * M[0] * Ep
C = C.change_ring(Zp)


def decompose(A, index_list, M, Ds):
    if len(A) == 0:
        return None
    elif len(A) == 1:
        if M != A[0]:
            return None
        else:
            return [index_list[0]]
    else:
        for i, Ai in enumerate(A):
            M_ = Ds^-1 * Ai^-1 * M
            MZ = M.change_ring(ZZ).list()
            MZ_ = M_.change_ring(ZZ).list()
            if (all(MZi_ < MZi for MZi, MZi_ in zip(MZ, MZ_))):
                A_ = A[:i] + A[i+1:]
                index_list_ = index_list[:i] + index_list[i+1:]
                res = decompose(A_, index_list_, M_, Ds)
                if res:
                    return [index_list[i]] + res
                else:
                    return None
        else:
            return None

def decrypt(C, M, As, Ep, Ds):
    T = Ep^-1 * C * Ep * Ds^-1
    # CAONIMA, exceed
    index_list = list(range(len(As)))
    for i, Ai in enumerate(As):
        A_ = As[:i] + As[i+1:]
        index_list_ = index_list[:i] + index_list[i+1:]
        T_ = Ds^-1 * Ai^-1 * T
        S = decompose(A_, index_list_, T_, Ds)
        if S:
            return [i] + S
    else:
        return None

my_order = decrypt(C, M, As, Ep, Ds)

from string import printable as prn
flag = 'CCTF{' + ''.join([prn[10 + my_order[_]] for _ in range(l)]) + '}'
print(f'{flag = }')