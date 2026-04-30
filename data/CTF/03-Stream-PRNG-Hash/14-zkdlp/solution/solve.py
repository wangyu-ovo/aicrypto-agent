from z3 import *
from random import Random
from itertools import count
from time import time
import logging
from helper import *

logging.basicConfig(format='STT> %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SYMBOLIC_COUNTER = count()
q = (p - 1) // 2


class Untwister:
    def __init__(self):
        name = next(SYMBOLIC_COUNTER)
        self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
        self.index = 0
        self.solver = Solver()

    # This particular method was adapted from https://www.schutzwerk.com/en/43/posts/attacking_a_random_number_generator/
    def symbolic_untamper(self, solver, y):
        name = next(SYMBOLIC_COUNTER)

        y1 = BitVec(f'y1_{name}', 32)
        y2 = BitVec(f'y2_{name}', 32)
        y3 = BitVec(f'y3_{name}', 32)
        y4 = BitVec(f'y4_{name}', 32)

        equations = [
            y2 == y1 ^ (LShR(y1, 11)),
            y3 == y2 ^ ((y2 << 7) & 0x9D2C5680),
            y4 == y3 ^ ((y3 << 15) & 0xEFC60000),
            y == y4 ^ (LShR(y4, 18))
        ]

        solver.add(equations)
        return y1

    def symbolic_twist(self, MT, n=624, upper_mask=0x80000000, lower_mask=0x7FFFFFFF, a=0x9908B0DF, m=397):
        '''
            This method models MT19937 function as a Z3 program
        '''
        MT = [i for i in MT]  # Just a shallow copy of the state

        for i in range(n):
            x = (MT[i] & upper_mask) + (MT[(i + 1) % n] & lower_mask)
            xA = LShR(x, 1)
            xB = If(x & 1 == 0, xA, xA ^ a)  # Possible Z3 optimization here by declaring auxiliary symbolic variables
            MT[i] = MT[(i + m) % n] ^ xB

        return MT

    def get_symbolic(self, guess):
        name = next(SYMBOLIC_COUNTER)
        ERROR = 'Must pass a string like "?1100???1001000??0?100?10??10010" where ? represents an unknown bit'

        assert type(guess) == str, ERROR
        assert all(map(lambda x: x in '01?', guess)), ERROR
        assert len(guess) <= 32, "One 32-bit number at a time please"
        guess = guess.zfill(32)

        self.symbolic_guess = BitVec(f'symbolic_guess_{name}', 32)
        guess = guess[::-1]

        for i, bit in enumerate(guess):
            if bit != '?':
                self.solver.add(Extract(i, i, self.symbolic_guess) == bit)

        return self.symbolic_guess

    def submit(self, guess):
        '''
            You need 624 numbers to completely clone the state.
                You can input less than that though and this will give you the best guess for the state
        '''
        if self.index >= 624:
            name = next(SYMBOLIC_COUNTER)
            next_mt = self.symbolic_twist(self.MT)
            self.MT = [BitVec(f'MT_{i}_{name}', 32) for i in range(624)]
            for i in range(624):
                self.solver.add(self.MT[i] == next_mt[i])
            self.index = 0

        symbolic_guess = self.get_symbolic(guess)
        symbolic_guess = self.symbolic_untamper(self.solver, symbolic_guess)
        self.solver.add(self.MT[self.index] == symbolic_guess)
        self.index += 1

    def get_random(self):
        '''
            This will give you a random.Random() instance with the cloned state.
        '''
        logger.debug('Solving...')
        start = time()
        self.solver.check()
        model = self.solver.model()
        end = time()
        logger.debug(f'Solved! (in {round(end - start, 3)}s)')

        # Compute best guess for state
        state = list(map(lambda x: model[x].as_long(), self.MT))
        result_state = (3, tuple(state + [self.index]), None)
        rr = Random()
        rr.setstate(result_state)
        return rr



from pwn import remote
g = 2

r = remote('127.0.0.1', 1337)
r.recvline()
xx = r.recvline()
print(xx)
y = int(xx[3:].strip().decode())
print(y)

record = []


def split_into_32bit_chunks(num):
    chunks = []
    for _ in range(64):
        chunks.append(num & 0xFFFFFFFF)  # 取最低 32 位
        num >>= 32  # 右移 32 位，繼續取下一組
    chunks.append('?' * 32)
    return chunks


def test():
    record = []
    for _ in range(17):
        r.sendlineafter(b't = ', str(1).encode())
        c = int(r.recvline()[3:].strip().decode())
        chunks = split_into_32bit_chunks(c)
        record.extend(chunks)

        r.sendlineafter(b's = ', str(1).encode())
        r.recvline()
    assert len(record) == 65 * 17
    return record


for _ in range(10000):
    record = test()
    # print(record)
    ut = Untwister()
    for i in range(65 * 17):
        if i % 65 != 64:
            ut.submit(bin(record[i])[2:])
        else:
            ut.submit(record[i])
    try:
        r2 = ut.get_random()
        for _ in range(10):
            c = r2.randrange(q)
            s = 1
            # g == t * y^c mod p
            tmp = pow(y, c, p)
            t = g * pow(tmp, -1, p) % p

            print(c, s, t)
            r.sendlineafter(b't = ', str(t).encode())
            print(r.recvline())

            r.sendlineafter(b's = ', str(s).encode())
            print(r.recvline())
        print(r.recvline().decode())
        print(r.recvline().decode())
    except:
        pass
