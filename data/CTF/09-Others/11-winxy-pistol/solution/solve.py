import hashlib
from pwn import process, remote
from tqdm import tqdm
from Crypto.Util.strxor import strxor
from time import sleep
from server import DEATH_CAUSES

PREFIX = b'you continue walking. turn to page '
SUFFIX = b'.'

def decrypt(k, enc):
	key = k.to_bytes(1024//8, 'big')
	pad = hashlib.shake_256(key).digest(len(enc))
	return strxor(pad, enc)

def get_io():
	# return process(['python', 'server.py'])
	return remote('127.0.0.1', 1337)

def recvlineafter(io, delim):
	io.recvuntil(delim)
	return io.recvline()

def sneak(c, t):
	while True:
		io = get_io()
		n = int(recvlineafter(io, b'n: '))
		x0 = int(recvlineafter(io, b'x0: '))
		v = (t + x0) % n
		io.sendlineafter(b'v: ', str(v).encode())
		c0 = bytes.fromhex(recvlineafter(io, b'c0: ').decode().strip())
		for cause in DEATH_CAUSES:
			die = f'you die of {cause}.'
			msg = die.encode().ljust(64, b'\x00')
			m = strxor(strxor(msg, c0), c).rstrip(b'\x00')
			if m.startswith(PREFIX) and m.endswith(SUFFIX) and m[len(PREFIX):-len(SUFFIX)].isdigit():
				io.sendlineafter(b'turn to page: ', str(0).encode())
				io.close()
				return int(m[len(PREFIX):-len(SUFFIX)])
		io.sendlineafter(b'turn to page: ', str(0).encode())
		io.close()

io = get_io()

for _ in tqdm(range(64)):
	first_msg = recvlineafter(io, b'n: ')
	print(first_msg)
	n = int(first_msg)
	x0 = int(recvlineafter(io, b'x0: '))
	x1 = int(recvlineafter(io, b'x1: '))
	v = x0
	io.sendlineafter(b'v: ', str(v).encode())
	c0 = bytes.fromhex(recvlineafter(io, b'c0: ').decode().strip())
	c1 = bytes.fromhex(recvlineafter(io, b'c1: ').decode().strip())

	m = decrypt(0, c0).rstrip(b'\x00')
	if m.startswith(PREFIX) and m.endswith(SUFFIX) and m[len(PREFIX):-len(SUFFIX)].isdigit():
		page = int(m[len(PREFIX):-len(SUFFIX)])
	else:
		page = sneak(c1, (v - x1))

	io.sendlineafter(b'turn to page: ', str(page).encode())

io.interactive()
