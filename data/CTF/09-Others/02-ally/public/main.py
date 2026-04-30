#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
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

def main():
    border = "┃"
    pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    pr(border, ".::  Ally is my best friend, help him to solve his tough task  ::.", border)
    pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    nbit = 14
    level, step = 0, 19
    while True:
        pr(border, f'Please send your {nbit}-bit prime:  ')
        p = sc().strip()
        try:
            p = int(p)
        except:
            die(border, 'Your input is not valid! Bye!!!')
        if isPrime(p) and p.bit_length() == nbit:
            pr(border, 'Send the solution of the following Diophantine equation in positive integers x, y')
            pr(border, f'{p} * (x - y)**3 = (x**2 + y) * (x + y**2)')
            xy = sc().strip().decode()
            try:
                x, y = [int(_) for _ in xy.split(',')]
            except:
                die(border, 'Your answer is not valid! Bye!!!')
            if p * (x - y)**3 == (x**2 + y) * (x + y**2) and x > 0 and y > 0:
                if level == step:
                    die(border, f'Congratz! You got the flag: {flag}')
                else:
                    pr(border, f'Good job, try the next step {level + 2}')
                    level += 1
                    nbit = int(1.2*nbit) + getRandomRange(0, 6)
            else:
                die(border, 'Your answer is not correct! Bye!!')
        else:
            die(border, 'Kidding me!? Bye!!')

if __name__ == '__main__':
    main()