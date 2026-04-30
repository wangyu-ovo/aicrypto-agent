from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import random
from pwn import *

seed = random.randint(0, 10 ** 6)
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
    return key.hex(), ciphertext.hex()

r = remote("127.0.0.1", 1337)

key_dict = {}

for i in range(10 ** 6):
    msg = b"Hello world"
    seed = i % (10 ** 6)
    encrypt(msg)
    i = i + 1
    key, enc_msg = encrypt(msg)
    key_dict[enc_msg] = key

for i in range(3):
    r.recvuntil(b"What would you like to do (1 - guess the key, 2 - encrypt a message)?")
    r.sendline(b"2")

    r.recvuntil(b"What is your message?")
    msg = b"Hello world"
    r.sendline(msg)

    r.recvuntil(b"Here is your encrypted message: ")
    enc_msg = str(r.recv()[:32], "utf-8")
    key = key_dict[enc_msg]

    r.sendline(b"1")
    r.recvuntil(b"What is your guess (in hex)?")
    r.sendline(bytes(key, "utf-8"))

r.recvuntil(b"Here is the flag: ")
print(str(r.recvline(), "utf-8")[:-1])