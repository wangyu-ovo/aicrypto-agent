import os
import struct
from base64 import b64decode, b64encode

from pwn import remote, xor
from tqdm import tqdm


def le_bytes_to_num(b: bytes) -> int:
    return int.from_bytes(b, "little")


def le_num_to_bytes(n: int, n_byte=16) -> bytes:
    return n.to_bytes(n_byte, "little")


def clamp(r: int) -> int:
    return r & 0x0FFFFFFC0FFFFFFC0FFFFFFC0FFFFFFF


def solve():
    _ = io.sendlineafter(b"[menu]> ", b"1")
    _ = io.sendlineafter(b"plaintext:", b64encode(b"\x00" * 64))
    _ = io.recvuntil(b"< ")
    ct1 = b64decode(io.recvline().strip())
    _ = io.sendlineafter(b"[menu]> ", b"2")
    _ = io.recvuntil(b"< ")
    mac2 = b64decode(io.recvline().strip())
    _ = io.sendlineafter(b"[menu]> ", b"3")
    _ = io.sendlineafter(b"aad:", b64encode(b"\x00" * 16))
    _ = io.recvuntil(b"< ")
    mac3 = b64decode(io.recvline().strip())
    _ = io.sendlineafter(b"[menu]> ", b"4")
    _ = io.sendlineafter(b"target:", b64encode(b"\x00" * 32 + b"\x01" + b"\x00" * 31))
    _ = io.recvuntil(b"< ")
    mac4 = b64decode(io.recvline().strip())
    _ = io.sendlineafter(b"[menu]> ", b"5")
    _ = io.sendlineafter(b"l:", b"0")
    _ = io.sendlineafter(b"r:", b"13")
    _ = io.recvuntil(b"< ")
    mac5 = b64decode(io.recvline().strip())
    # ct1, _ = encrypt(key, aad, b"\x00" * 64, nonce)
    # _, mac2 = encrypt(key, aad, plaintext, nonce)
    # _, mac3 = encrypt(key, b"\x00" * 16, plaintext, nonce)
    # _, mac4 = encrypt(key, aad, xor(plaintext, b"\x00"*32 + b"\x01" + b"\x00"*31), nonce)
    # _, mac5 = encrypt(key, aad, plaintext[0: 13], nonce)  # ct5 == ct1[:13]

    # mac2, mac4 から r を求める
    # ((aad + 2**128) * r**6 + (c1 + 2**128) * r**5 + (c2 + 2**128) * r**4 + (c3 + 2**128) * r**3 + (c4 + 2**128) * r**2 + (L + 2**128) * r % p) + s - k * 2**128 (0 <= k <= 4)
    p = 2**130 - 5
    r_cands = []
    for k in range(-4, 5):
        if ct1[32] % 2 == 0:
            roots = Zmod(p)(
                le_bytes_to_num(mac4) - le_bytes_to_num(mac2) + k * 2**128
            ).nth_root(3, all=True)
        else:
            roots = Zmod(p)(
                le_bytes_to_num(mac2) - le_bytes_to_num(mac4) + k * 2**128
            ).nth_root(3, all=True)
        assert len(roots) == 1
        root = int(roots[0])
        if root.bit_length() <= 128:
            r_cands.append(root)
            # print(root)

    # mac3 から a を求める
    # a * r**6 == le_bytes_to_num(mac2) - le_bytes_to_num(mac3) + k * 2**128 mod 2**130-5
    # a = le_bytes_to_num(aad)
    ar_cands = []
    for _r in r_cands:
        for k in range(-4, 5):
            rhs = le_bytes_to_num(mac2) - le_bytes_to_num(mac3) + k * 2**128
            root = int(rhs * pow(_r, -6, p) % p)
            if root.bit_length() > 128:
                continue
            tmp = le_num_to_bytes(root)
            try:
                tmp = tmp.decode()
            except UnicodeDecodeError:
                continue
            ar_cands.append((root, _r))
    # print(ar_cands)
    if len(ar_cands) == 1:
        a, r = ar_cands[0]
    else:
        print("yarinaoshi")

    # mac5 から s を求める
    tmp = (a + 2**128) * r**3
    tmp += (le_bytes_to_num(ct1[:13] + b"\x00" * 3) + 2**128) * r**2
    tmp += (
        le_bytes_to_num(struct.pack("<Q", 16) + struct.pack("<Q", 13)) + 2**128
    ) * r
    tmp %= p
    s = (le_bytes_to_num(mac5) - tmp) % 2**128

    # ct1 と mac2 から cipehrtext を求める
    # [1, c1, c2, c3, c4, k128, 0] = [1, c1, c2, c3, c4, k128, kp] * mat
    mat = matrix(ZZ, 7, 7)
    for i in range(6):
        mat[i, i] = 1
    mat[0, 6] = (
        (a + 2**128) * r**6
        + (le_bytes_to_num(ct1[:13] + b"\x00" * 3) + 2**128) * r**5
        + (le_bytes_to_num(ct1[16:29] + b"\x00" * 3) + 2**128) * r**4
        + (le_bytes_to_num(ct1[32:45] + b"\x00" * 3) + 2**128) * r**3
        + (le_bytes_to_num(ct1[48:61] + b"\x00" * 3) + 2**128) * r**2
        + (le_bytes_to_num(struct.pack("<Q", 16) + struct.pack("<Q", 64)) + 2**128)
        * r
        + s
        - le_bytes_to_num(mac2)
    )
    mat[1, 6] = 2**104 * r**5
    mat[2, 6] = 2**104 * r**4
    mat[3, 6] = 2**104 * r**3
    mat[4, 6] = 2**104 * r**2
    mat[5, 6] = -(2**128)
    mat[6, 6] = -p
    weights = diagonal_matrix(
        [256**3] + [1] * 4 + [256**3 // 4] + [int(256**3 * sqrt(7))]
    )
    mat *= weights
    L = mat.LLL()
    L /= weights
    mat /= weights
    if L[0, 0] == -1:
        L = -L
    assert L[0, 0] == 1
    assert L[0, -1] == 0
    ciphertext = (
        ct1[:13]
        + le_num_to_bytes(int(L[0, 1]), 3)
        + ct1[16:29]
        + le_num_to_bytes(int(L[0, 2]), 3)
        + ct1[32:45]
        + le_num_to_bytes(int(L[0, 3]), 3)
        + ct1[48:61]
        + le_num_to_bytes(int(L[0, 4]), 3)
    )
    plaintext = xor(ct1, ciphertext)

    _ = io.sendlineafter(b"[menu]> ", b"6")
    _ = io.sendlineafter(b"answer:", b64encode(plaintext))


if __name__ == "__main__":
    set_verbose(0)
    # io = remote("muck-a-mac.int.seccon.games", int(8080))
    io = remote('127.0.0.1', int(1337))
    for _ in tqdm(range(100)):
        solve()
    _ = io.recvline()
    _ = io.recvline()
    print(io.recvline())
