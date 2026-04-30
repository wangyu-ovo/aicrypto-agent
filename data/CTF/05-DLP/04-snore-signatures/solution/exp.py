from pwn import *
from Crypto.Util.number import *

r = remote('127.0.0.1', 1337)


def rn():
    return int(r.recvline().decode('ascii').split('= ')[-1][:-1])


p = rn()
q = rn()
g = rn()

for i in range(10):
    r.recvuntil(b'y = ').decode('ascii')
    y = rn()

    m = i
    r.sendlineafter(b'm = ', str(m).encode())

    s = rn()
    e = rn()

    o_rv = (pow(g, s, p) * pow(y, e, p)) % p

    s += 1

    n_rv = (pow(g, s, p) * pow(y, e, p)) % p

    n_m = ((o_rv - n_rv) + m) % p

    r.sendlineafter(b'm = ', str(n_m).encode())
    r.sendlineafter(b's = ', str(s).encode())

r.interactive()
