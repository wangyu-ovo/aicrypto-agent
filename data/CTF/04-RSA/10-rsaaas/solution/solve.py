from Crypto.Util.number import getPrime
from pwn import *

p = getPrime(64)
while p % 65537 != 1:
    p = getPrime(64)
q = getPrime(64)

print(p)
print(q)

io = remote('127.0.0.1', 1337)
io.recvuntil('Input p: ')
io.sendline(str(p))
io.recvuntil('Input q: ')
io.sendline(str(q))
io.interactive()
