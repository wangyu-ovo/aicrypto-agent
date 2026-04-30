from pwn import *
import hashlib
import os
import binascii
from tqdm import tqdm

context.log_level = 'error'


# s is 16 bits long, 32 bit output
def PRG(s: bytes) -> bytes:
    assert len(s) == 2, "You're trying to cheat! Go to Crypto Prison!"
    s_int = int.from_bytes(s, byteorder="big")
    h = hashlib.new("sha3_256")
    h.update(s)
    out = h.digest()
    return out[:4]


dic = {}
for i in range(256):
    for j in range(256):
        k = bytes([i, j])
        dic[PRG(k)] = k

p = remote('127.0.0.1', 1337)
cnt = 0
for _ in tqdm(range(200)):
    p.recvuntil(b"Here's y: ")
    y = bytes.fromhex(p.recvline().decode()[:-1])
    # y = os.urandom(4)
    print(f"{y.hex() = }")
    for k in dic:
        k2 = xor(k, y)
        if k2 in dic:
            print('got: ', dic[k2].hex(), k2.hex())
            key1 = k2
            ans1 = dic[key1]
            key0 = k
            ans0 = dic[key0]
            ok = 1
            break
        else:
            key1 = b'AA'
            ans1 = b'AA'
            key0 = k
            ans0 = dic[k]
            ok = 0
            pass

    print('com:',k.hex())
    p.sendlineafter(b'>', k.hex().encode())

    msg = p.recvline()
    print('choice:',msg)

    if b'chicken?' in msg:
        choice = 0
    else:
        choice = 1

    # choice = int.from_bytes(os.urandom(1), byteorder="big") & 1
    if choice == 0:
        p.sendlineafter(b'>', ans0.hex().encode())
        cnt += 1
    else:
        p.sendlineafter(b'>', ans1.hex().encode())
        cnt += ok
    print(_, choice, cnt)
print(p.recvline())
p.interactive()