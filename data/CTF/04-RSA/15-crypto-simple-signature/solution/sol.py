from pwn import *

r = remote("127.0.0.1", 1337)

r.recvuntil(b"n = ")
n = int(r.recvline()[:-1])

r.recvuntil(b"e = ")
e = int(r.recvline()[:-1])

r.recvuntil(b"Enter a message as an integer (enter 0 to stop):")
r.sendline(b"1")

r.recvuntil(b"Enter a message as an integer (enter 0 to stop):")
r.sendline(b"4")

r.recvuntil(b"Your signature is: ")
s = r.recvline()[:-1]

r.recvuntil(b"Enter a message as an integer (enter 0 to stop):")
r.sendline(b"0")

r.recvuntil(b"Enter a message: ")
r.sendline(b"3")

r.recvuntil(b"Enter a signature: ")
r.sendline(s)

r.recvuntil(b"Congrats! Here is the flag: ")
print(str(r.recvline(), "utf-8")[:-1])