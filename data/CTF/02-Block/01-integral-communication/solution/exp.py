from pwn import *
from Crypto.Util.strxor import strxor
import binascii

p = remote('127.0.0.1', 1337)

# Step 1: Create initial command
p.sendlineafter(b'> ',b'1')
p.sendlineafter(b': ', b'\n')
p.recvuntil(b': ')
iv = p.recvuntil(b'\n')[:-1]
p.recvuntil(b': ')
p.recvuntil(b': ')
cmd = p.recvuntil(b'\n')[:-1].decode('ascii')

cmd = binascii.unhexlify(cmd) # command = "{"from": "guest", "act": "echo", "msg": ""}"

# Step 2: Forge first 16 bytes of command to change "echo" to "flag"
forged_cmd_part = strxor(cmd[:16], b'\x00' * 10 + strxor(b'echo', b'flag') + b'\x00' * 2)
forged_cmd = binascii.hexlify(forged_cmd_part + cmd[16:])

p.sendlineafter(b'> ',b'2')
p.sendlineafter(b': ', iv)
p.sendlineafter(b': ', forged_cmd)

# Step 3: Use error message telling us the decrypted message to forge iv to fix first 16 bytes of message and change "guest" to "admin"
p.recvuntil(b': ')
decrypted_cmd = p.recvuntil(b'\n')[:-1]
print(decrypted_cmd)
cmd_block1 = binascii.unhexlify(decrypted_cmd[:32])
print(decrypted_cmd[:32])
forged_iv = strxor(binascii.unhexlify(iv), strxor(cmd_block1, b'{"from": "admin"'))
forged_iv = binascii.hexlify(forged_iv)

p.sendlineafter(b'> ',b'2')
p.sendlineafter(b': ', forged_iv)
p.sendlineafter(b': ', forged_cmd)

p.interactive()
