
from pwn import *

from Crypto.Util.strxor import strxor

con = remote('127.0.0.1', 1337)

con.recvuntil(b'you have one new encrypted message:\n')
msg = bytes.fromhex(con.recvline().strip().decode())


def get_encryption(block):
    con.recvuntil(b' > ')
    con.sendline(block.hex().encode())
    h = con.recvline().decode().strip()
    return bytes.fromhex(h)[-16:]


encrypted = []
pt = [msg[0:16]]
for i in range(0, len(msg) - 16, 16):
    encrypted.append(get_encryption(pt[-1]))
    pt.append(strxor(encrypted[-1], msg[i+16:i+32]))
print(b''.join(pt[1:-1]).decode())
