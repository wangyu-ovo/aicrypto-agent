from Crypto.Util.number import *
from tqdm import trange
load('./helper.sage')


n = 24
q = 223^24 - 1
msg_ = b''
for C in enc:
    C_ = C
    for t in trange(1, n):
        C_ -= pubkey[-t]
        for C__ in range(C_, C_ + n * q, q):
            L = [[0 for j in range(n+3)] for i in range(n+1)]
            for i in range(n):
                L[i][i] = 1
                L[i][n+1] = 1
                L[i][n+2] = pubkey[i]
            L[n][n] = 1
            L[n][n+1] = t - 24
            L[n][n+2] = -C__
            L = matrix(ZZ, L)
            for vline in L.LLL():
                if vline[n] < 0:
                    vline = -vline
                if vline[n] == 1:
                    if all(x in {0, 1} for x in vline[:n]):
                        print('AOLIGEI!!!')
                        msg = ''.join(map(str, vline[:n].list()))
                        msg = long_to_bytes(int(msg, 2))
                        print(msg)
                        msg_ += msg
                        break
            else:
                continue
            break
        else:
            continue
        break
    else:
        raise Exception(f'GG {C = }')

print(msg_)

'''
real    5m21.739s
user    5m10.547s
sys     0m10.987s
'''