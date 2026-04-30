from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time
from pwn import *

t = time.time()
seed = int(t * 1000) % (10 ** 6)
def get_random_number():
    global seed
    seed = int(str(seed * seed).zfill(12)[3:9])
    return seed

def encrypt(message):
    key = b''
    for i in range(8):
        key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(message, AES.block_size))
    return ciphertext.hex()

def decrypt(ciphertext_hex):
    key = b''
    for i in range(8):
        key += (get_random_number() % (2 ** 16)).to_bytes(2, 'big')
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted = cipher.decrypt(ciphertext)
    unpadded = unpad(decrypted, AES.block_size)

    return unpadded.decode('utf-8')

r = remote("127.0.0.1", 1337)

r.recvuntil(b"What would you like to do (1 - get encrypted flag, 2 - encrypt a message)?")
r.sendline(b"2")

r.recvuntil(b"What is your message?")
msg = b"Hello world"
r.sendline(msg)

r.recvuntil(b"Here is your encrypted message: ")
enc_msg = str(r.recv()[:32], "utf-8")
exp_enc_msg = encrypt(msg)
i = 0

while exp_enc_msg != enc_msg:
    seed = int(t * 1000) % (10 ** 6) + i
    i = i + 1
    exp_enc_msg = encrypt(msg)

r.sendline(b"1")
r.recvuntil(b"Here is the encrypted flag: ")
enc_flag = str(r.recv()[:-1], "utf-8")

print(decrypt(enc_flag))