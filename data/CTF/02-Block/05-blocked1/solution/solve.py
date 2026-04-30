
from pwn import *

from Crypto.Util.strxor import strxor

# con = process('python3 ../challenge/server.py', shell=True)
con = remote('127.0.0.1', 1337)

con.recvuntil(b'you are logged in as: ')
username = con.recvline().strip()


def pad(msg):
    if len(msg) % 16 != 0:
        msg += b'\x00' * (16 - len(msg) % 16)
    return msg


difference = strxor(pad(username), pad(b'doubledelete'))

con.recvuntil(b'> ')
con.sendline(b'2')
token = con.recvline().decode().strip()
print(token)
token = bytes.fromhex(token)

new_token = strxor(token, b'\x00' * 16 + difference + b'\x00' * 16)

con.recvuntil(b'> ')
con.sendline(b'1')
con.sendline(new_token.hex().encode())
con.interactive()
