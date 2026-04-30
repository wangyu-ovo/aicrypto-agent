import binascii
from sage.all import *
from pwn import *

while True:
    io = remote('127.0.0.1', 51375)
    io.recvuntil('Pseudo_n =  ')
    pseudo_n = int(io.recvline())
    io.recvuntil('Ciphertext 1 = ')
    c1 = int(io.recvline())
    io.recvuntil('Ciphertext 2 = ')
    c2 = int(io.recvline())
    io.recvuntil('Ciphertext 3 = ')
    c3 = int(io.recvline())

    lucky_l = []
    for i in range(9, 14, 1):
        io.recvuntil('Enter your lucky number :')
        io.sendline(str(i))
        io.recvuntil('Your lucky output :')
        lucky_l.append(int(io.recvline()))
    io.close()
    k = 13
    e =  27525540
    for lucky in lucky_l:
        large = lucky * factorial(k - 1) * factorial(k) + 1
        r = gcd(large, pseudo_n)
        if r != 1:
            break
    if r > 10000:
        print('r:', r)
        print(large / r)
        print("large / r:", factor(large / r))

        p = factor(large / r)[-1][0]
        if gcd(e//4, p - 1) != 1:
            continue
        d = pow(e // 4, -1, p - 1)

        flag = binascii.unhexlify(hex(isqrt(pow(c1, d * (p + 1) // 4, p)))[2:]) + binascii.unhexlify(hex(isqrt(pow(c2, d * (p + 1) // 4, p)))[2:]) + binascii.unhexlify(hex(isqrt(pow(c3, d * (p + 1) // 4, p)))[2:])
        print(flag)
        if b'BITSCTF' not in flag:
            continue
        break
    else:
        continue