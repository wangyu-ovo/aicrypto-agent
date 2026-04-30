#!/usr/bin/env python3

from pwn import *

import warnings
warnings.filterwarnings("ignore")

HOST = '127.0.0.1'
PORT = 1337

p = remote(HOST, PORT)

string1 = b'61616161616161616161616161616161'
string2 = b'61616161616161616161616161616162'

for i in range(5):
    print(p.readline().decode('utf-8'), end='')

for i in range(128):
    p.writelineafter('Action: ', b'1')
    p.writelineafter('m0 (16 byte hexstring): ', string1)
    p.writelineafter('m1 (16 byte hexstring): ', string2)
    encrypt = p.readline().decode('utf-8').strip('\n')
    print(encrypt)
    p.writelineafter('Action: ', b'2')
    p.writelineafter('ct (512 byte hexstring): ', encrypt)
    decrypt = p.readline().decode('utf-8').strip('\n')
    print(decrypt)
    if decrypt == string1.decode('utf-8'):
        guess_bit = b'0'
    else:
        guess_bit = b'1'
    print(f'Guess bit: {guess_bit}')
    p.writelineafter('Action: ', b'0')
    p.writelineafter('m_bit guess: ', guess_bit)
    print(p.readline())

print(p.read())