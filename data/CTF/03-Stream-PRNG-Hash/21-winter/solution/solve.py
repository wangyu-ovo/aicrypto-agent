# import os
# from hashlib import sha256
# from tqdm import tqdm
#
# msg = os.urandom(32)
# for _ in tqdm(range(2**32)):
# 	m = sha256(msg).digest()
# 	for n in m:
# 		if n >= 128:
# 			break
# 	else:
# 		print('low', msg.hex())
# 	msg = m

from pwn import process, remote
from main import Wots

low = 'c742884474188078e2059c928d2483158d1376e07768c8607fc5cbc70062ceb2'
high = '0442fc6482900446168ea4c1f616be85c2502dfee755d427623d5aecb20dcad7'

io = remote('127.0.0.1', 1337)

io.sendlineafter(': ', high.encode())
io.recvuntil(': ')
sig1 = bytes.fromhex(io.recvline().decode())

m1 = Wots.hash(bytes.fromhex(low), 1)
m2 = Wots.hash(bytes.fromhex(high), 1)
chunks = [sig1[i:i+32] for i in range(0, len(sig1), 32)]
sig2 = b''.join([Wots.hash(x, n2 - n1) for x, n1, n2 in zip(chunks, m1, m2)])

io.sendlineafter(': ', low.encode())
io.sendlineafter(': ', sig2.hex().encode())
io.interactive()
