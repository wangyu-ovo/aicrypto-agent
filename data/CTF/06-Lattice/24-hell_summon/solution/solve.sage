import os
os.environ['TERM'] = 'linux'
import random

from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.strxor import strxor
from pwn import remote

# download from: https://raw.githubusercontent.com/maple3142/lll_cvp/refs/heads/master/lll_cvp.py
from lll_cvp import *


def encrypt(message,priv):
    chunk_size = 5
    p,r,H = priv
    assert len(message) % 5 == 0

    message_chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

    ciphertext = b""
    mac = 0
    for chunk in message_chunks:
        temp = strxor(chunk, H)
        mac = (r*(mac + bytes_to_long(temp))) % p
        ciphertext += temp

    return ciphertext, long_to_bytes(mac)


max_retry = 16

while True:
    io = remote('127.0.0.1', int(44092))
    _ = io.recvuntil(b"p=")
    p = int(io.recvline())
    _ = io.recvuntil(b"messages=")
    messages = eval(io.recvline().strip().decode())
    _ = io.recvuntil(b"truncated_macs=")
    truncated_macs = eval(io.recvline().strip().decode())

    ms = [int(m, 16) for m in messages]
    ts = [int(t, 16) for t in truncated_macs]


    for _ in range(max_retry):
        h_zero_idx = random.choices(range(40), k=3)
        """
        r * ((m_i - m_j) - 2 * ((m_i & H) - (m_j & H))) % p == (t_i - t_j) * 2**16 + (s_i - s_j)
        2 * r * (m_i & H) = 2 * r * \sum_j (m_i_j * H_j * 2**j)
        """
        # [rH1, ..., rHL, s1, ..., sM, r, 1] = [rH1, ..., rHL, k1, ..., kM, r, 1] * mat
        L = 40 - len(h_zero_idx)
        M = 42 - 1
        mat = matrix(ZZ, L+M+2, L+M+2)
        lb = []
        ub = []
        for i in range(L):
            mat[i, i] = 1
            lb.append(0)
            ub.append(2**64)
        for i in range(M):
            for j in range(40):
                if j in h_zero_idx:
                    continue
                mat[j, L+i] = -2 * (((ms[i] >> j & 1) - (ms[-1] >> j & 1)) << j)
            mat[L+i, L+i] = -p
            mat[L+M, L+i] = ms[i] - ms[-1]
            mat[L+M+1, L+i] = -(ts[i] - ts[-1]) * 2**16
            lb.append(-2**16)
            ub.append(2**16)
        mat[L+M, L+M] = 1
        mat[L+M+1, L+M+1] = 1
        lb += [0, 1]
        ub += [2**64, 1]
        res = solve_inequality(mat, lb, ub)
        r_rec = int(res[-2])
        print(r_rec)
        if r_rec > 0:
            break
    else:
        io.close()
        continue

    r = r_rec

    """
    r * ((m_i - m_j) - 2 * ((m_i & H) - (m_j & H))) % p == (t_i - t_j) * 2**16 + (s_i - s_j)
    2 * r * (m_i & H) = 2 * r * \sum_j (m_i_j * H_j * 2**j)
    """
    # [H1, ..., HL, s1, ..., sM, 1] = [H1, ..., HL, k1, ..., kM, 1] * mat
    L = 40
    M = 42 - 1
    mat = matrix(ZZ, L+M+1, L+M+1)
    lb = []
    ub = []
    for i in range(L):
        mat[i, i] = 1
        lb.append(0)
        ub.append(1)
    for i in range(M):
        for j in range(40):
            # if j in h_zero_idx:
            #     continue
            mat[j, L+i] = -2 * (((ms[i] >> j & 1) - (ms[-1] >> j & 1)) << j) * r
        mat[L+i, L+i] = -p
        mat[L+M, L+i] = r * (ms[i] - ms[-1]) - (ts[i] - ts[-1]) * 2**16
        lb.append(-2**16)
        ub.append(2**16)
    mat[L+M, L+M] = 1
    lb += [1]
    ub += [1]
    res = solve_inequality(mat, lb, ub)
    h_rec = int(sum([res[i] * 2**i for i in range(40)]))
    H = long_to_bytes(h_rec, 5)
    print(H)

    ct, mac = encrypt(b"Kurenaif,gimme flag!", (p, r, H))

    io.sendlineafter(b"ciphertext:", ct.hex().encode())
    io.sendlineafter(b"mac:", mac.hex().encode())
    try:
        print(io.recvline())
        break
    except EOFError:
        io.close()
        continue