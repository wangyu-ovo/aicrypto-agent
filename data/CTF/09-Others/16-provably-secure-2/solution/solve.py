#!/usr/bin/env python3

from pwn import *
from Crypto.Util.strxor import strxor

import warnings
warnings.filterwarnings("ignore")

HOST = '127.0.0.1'
PORT = 1337

p = remote(HOST, PORT)

string1 = b'61616161616161616161616161616161'
string2 = b'61616161616161616161616161616162'
string3 = b'61616161616161616161616161616163'
string4 = b'61616161616161616161616161616164'

xor1    = b'00000000000000000000000000000002'

for i in range(5):
    print(p.readline().decode('utf-8'), end='')

for i in range(128):
    p.writelineafter('Action: ', b'1')
    p.writelineafter('m0 (16 byte hexstring): ', string1)
    p.writelineafter('m1 (16 byte hexstring): ', string2)
    ct1 = p.readline().decode('utf-8').strip('\n')
    print(ct1)

    p.writelineafter('Action: ', b'1')
    p.writelineafter('m0 (16 byte hexstring): ', string3)
    p.writelineafter('m1 (16 byte hexstring): ', string4)
    ct2 = p.readline().decode('utf-8').strip('\n')
    print(ct2)

    ctnew = bytes.fromhex(ct1.strip())[:256].hex() + bytes.fromhex(ct2.strip())[256:].hex()
    p.writelineafter('Action: ', b'2')
    p.writelineafter('ct (512 byte hexstring): ', ctnew)
    pt1 = p.readline().decode('utf-8').strip('\n')
    print(pt1)

    ctnew2 = bytes.fromhex(ct2.strip())[:256].hex() + bytes.fromhex(ct1.strip())[256:].hex()
    p.writelineafter('Action: ', b'2')
    p.writelineafter('ct (512 byte hexstring): ', ctnew2)
    pt2 = p.readline().decode('utf-8').strip('\n')
    print(pt2)

    if strxor(bytes.fromhex(pt1), bytes.fromhex(pt2)).hex() == xor1.decode('utf-8'):
        guess_bit = b'0'
    else:
        guess_bit = b'1'
    print(f'Guess bit: {guess_bit}')
    p.writelineafter('Action: ', b'0')
    p.writelineafter('m_bit guess: ', guess_bit)
    print(p.readline())

print(p.read())