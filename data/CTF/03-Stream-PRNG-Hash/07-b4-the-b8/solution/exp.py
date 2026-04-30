from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.number import *

p = remote('127.0.0.1', 1337)
n = 1024
bell = [b"0.5"] + [b"0"] * 2 + [b"0.5"] + [b"0"] * 8 + [b"0.5"] + [b"0"] * 2 + [b"0.5"]
for i in range(n * 5 // 8):
    p.sendline(b"3")
    p.sendline(b"0")
for i in range(n * 3 // 8):
    p.sendline(b"2")
    for coeff in bell:
        p.sendline(coeff)
    p.sendline(b"3")
    p.sendline(str(385 + i))
p.recvuntil(b"My bases were ")
b_bases = int(p.recvline()[:-1], 2)
p.recvuntil(b"my bases were ")
a_bases = int(p.recvline()[:-1], 2)
p.recvuntil(b"looks good.\n")
a_iv = p.recvline()[:-1]
print(f'a_iv: {a_iv}')
b_iv = p.recvline()[:-1]
print(f'b_iv: {b_iv}')
ciphertext = p.recvline()[:-1]
Alice_results = b""
Bob_results = b""
for i in range(n * 3 // 8):
    p.sendline(b"1")
    p.sendline(str((a_bases >> (n * 5 // 8 + i)) & 1))
    p.sendline(str(i))
    p.recvuntil(b"result is: ")
    Alice_results = p.recvline()[:-1] + Alice_results
Alice_results = int(Alice_results, 2)
for i in range(n * 3 // 8):
    p.sendline(b"1")
    p.sendline(str((b_bases >> (n * 5 // 8 + i)) & 1))
    p.sendline(str(n * 3 // 8 + i))
    p.recvuntil(b"result is: ")
    Bob_results = p.recvline()[:-1] + Bob_results
Bob_results = int(Bob_results, 2)
Alice_key = ""
Bob_key = ""
count = 0
for i in range(n * 3 // 8):
    if ((a_bases >> (n * 5 // 8 + i)) & 1) == ((b_bases >> (n * 5 // 8 + i)) & 1):
        Alice_key = Alice_key + str((Alice_results >> i) & 1)
        Bob_key = Bob_key + str((Bob_results >> i) & 1)
        count += 1
Alice_key = int(Alice_key[-128:], 2)
Bob_key = int(Bob_key[-128:], 2)
aes_alice = AES.new(Alice_key.to_bytes(length=16, byteorder='big'), AES.MODE_CBC, iv=int(a_iv, 16).to_bytes(length=16, byteorder='big'))
aes_bob = AES.new(Bob_key.to_bytes(length=16, byteorder='big'), AES.MODE_CBC, iv=int(b_iv, 16).to_bytes(length=16, byteorder='big'))
flag = aes_alice.decrypt(aes_bob.decrypt(int(ciphertext, 16).to_bytes(length=len(ciphertext)//2, byteorder='big')))
print(flag)