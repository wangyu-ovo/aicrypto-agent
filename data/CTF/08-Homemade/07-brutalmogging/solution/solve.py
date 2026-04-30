import os
import string
from hashlib import sha256
from pwn import *

def xor(data1, data2):
    return bytes([data1[i] ^ data2[i] for i in range(len(data1))])

def do_round(data, key):
    m = sha256()
    m.update(xor(data[2:4], key))
    return bytes(data[2:4]) + xor(m.digest()[0:2], data[0:2])

def do_round_inv(data, key):
    m = sha256()
    m.update(xor(data[0:2], key))
    return xor(m.digest()[0:2], data[2:4]) + bytes(data[0:2])

def pad(data):
    padding_length = 4 - (len(data) % 4)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    padding_length = data[-1]
    return data[:-padding_length]

# XOR every character with bytes generated from the PRNG
def encrypt_block(data, key):
    
    for i in range(10):
        data = do_round(data, key)
    return data

def decrypt_block(data, key):
    for i in range(10):
        data = do_round_inv(data, key)
    return data

def encrypt_data(data, key):
    cipher = b''
    while data:
        cipher += encrypt_block(data[:4], key)
        data = data[4:]
    return cipher

def decrypt_data(cipher, key):
    data = b''
    while cipher:
        data += decrypt_block(cipher[:4], key)
        cipher = cipher[4:]
    return data

def encrypt(data, key):
    data = pad(data)
    return encrypt_data(encrypt_data(data, key[0:2]), key[2:4])

def decrypt(data, key):
    plain = decrypt_data(decrypt_data(data, key[2:4]), key[0:2])
    return unpad(plain)

if __name__ == '__main__':
    io = remote('127.0.0.1', 1337)
    io.recvuntil('The encrypted flag is: ')
    FLAG = bytes.fromhex(io.recvline().decode())
    flags = [pad(flag) for flag in [b'1', b'12', b'123']]
    ciphers = []
    for fi in [b'1', b'12', b'123']:
        io.recvuntil(': ')
        io.sendline(fi)
        io.recvuntil(': ')
        ciphers.append(io.recvline().decode())
    ciphers = [bytes.fromhex(hexval) for hexval in ciphers]

    found_left = []
    found_right = []
    for i in range(256):
        for j in range(256):
            found_left.append(tuple([ encrypt_data(flag, bytes([i, j])) for flag in flags ]))
            found_right.append(tuple([ decrypt_data(cipher, bytes([i, j])) for cipher in ciphers ]))

    matching_pairs = set(found_left).intersection(set(found_right))
    possible_keys = []
    for pair in matching_pairs:
        left_key = found_left.index(pair)
        right_key = found_right.index(pair)
        possible_keys.append(bytes([left_key >> 8, left_key & 0xff, right_key >> 8, right_key & 0xff]))

    for index, keys in enumerate(possible_keys):
        print(keys.hex())
        plain = [decrypt(cipher, keys) for cipher in ciphers]
        FLAG_plain = decrypt(FLAG, keys)
        print(f"[{index}] {keys.hex()} {plain}: {FLAG_plain}")