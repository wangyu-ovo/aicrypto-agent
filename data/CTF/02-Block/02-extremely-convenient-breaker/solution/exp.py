from pwn import *

io = remote('127.0.0.1', 1337)

io.recvuntil(b'hex:')
io.recvline()
ct_hex  = io.recvline().strip().decode()

ct = bytes.fromhex(ct_hex)
flag = ''
for i in range(0, len(ct), 16):
    x = ct[i:i+16]
    x = x + b'\x00' * (64 - len(x))
    # io.interactive()
    io.sendlineafter(b'hex',x.hex())
    x = (io.recvline().strip().decode())
    flag+=x[:20]

print(flag)
# lactf{seems_it_was_extremely_convenient_to_get_the_flag_too_heh}