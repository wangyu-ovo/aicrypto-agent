from pwn import *

p = remote('127.0.0.1', 1337)
prefix = 'GET FILE: flag.txt'

p.sendline(b'a'*16)
p.sendline(b'a')
tag = p.recvline()[:-1]
print(tag)

payload = prefix.encode() + b'a'*(16 - (len(prefix) % 16)) + b'a'*16
assert len(payload) % 16 == 0

p.sendline(payload)
p.sendline(tag)
print(p.recvrepeat(1))