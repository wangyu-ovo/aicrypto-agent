#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
from string import *
from random import *
from flag import flag

def die(*args):
    pr(*args)
    quit()

def pr(*args):
    s = " ".join(map(str, args))
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def sc(): 
    return sys.stdin.buffer.readline()

def randstr(l):
    return ''.join([printable[randint(0, 90)] for _ in range(l)])

def encrypt(msg, p, q):
    e = 65537
    m1, m2 = msg[:len(msg) >> 1], msg[len(msg) >> 1:]
    m1, m2 = bytes_to_long(m1), bytes_to_long(m2)
    c1, c2 = pow(m1, e, (p - 1) * (q - 1)), pow(m2, e, (2*p + 1) * (2*q + 1))
    return (c1, c2)

def main():
    border = "┃"
    pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    pr(border, ".: Welcome to RM2 task! Your mission is break our cryptosystem :. ", border)
    pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    nbit, _b = 1024, False
    pr(border, f"Please provide your desired {nbit}-bit prime numbers p, q:")
    inp = sc().decode()
    try:
        p, q = [int(_) for _ in inp.split(',')]
        if p.bit_length() == q.bit_length() == nbit and isPrime(p) and isPrime(q) and p != q:
            _b = True
    except:
        die(border, f"The input you provided is is not valid!")
    if _b:
        e, n =  65537, p * q
        s = randstr(nbit >> 4).encode()
        m = bytes_to_long(s)
        assert m < n >> 2
        c1, c2 = encrypt(s, p, q)
        pr(border, f'c1 = {c1}')
        pr(border, f'c2 = {c2}')
        pr(border, f'Now, send us the secret string to get the flag: ')
        _m = sc().strip()
        if _m == s:
            die(border, f'Congrats, you got the flag: {flag}')
        else:
            die(border, f'The secret string is not correct! Bye!!')
    else:
        die(border, f"Your input does not meet the requirements!!!")

if __name__ == '__main__':
    main()