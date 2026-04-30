from z3 import *
from helper import *

nsteps = 2048
n = 256
s = Solver()
xs = [BitVec(f'x{i}', n) for i in range(nsteps)]
carry = [Bool(f'carry{i}') for i in range(nsteps - 1)]
for i in range(2):
    s.add(URem(xs[i], 3) == stream[i])

for i in range(nsteps - 1):
    tmp = LShR(xs[i], 1)
    tmp = If(carry[i], tmp | 1 << (n - 1), tmp)
    s.add(xs[i + 1] == tmp)
    for lsb in range(2):
        for carried in [False, True]:
            rightval = (stream[i + 1] * 2 + lsb + (2 if carried else 0)) % 3
            if rightval != stream[i]:
                s.add(Or(xs[i] & 1 != lsb, carry[i] != carried))

r = s.check()
print(f'{r = }')
if r == unsat:
    print('Nothing to be done')
    exit(1)

proof = s.model()
print(proof[xs[0]])
seed = proof.eval(xs[0]).as_long()

class LF3R:
    def __init__(self, n, key, mask):
        self.n = n
        self.state = key & ((1 << n) - 1)
        self.mask = mask

    def __call__(self):
        v = self.state % 3
        self.state = (self.state >> 1) | (
            ((self.state & self.mask).bit_count() & 1) << (self.n - 1)
        )
        return v


def int_to_base(n, b):
    digits = []
    while n:
        digits.append(n % b)
        n //= b
    return digits

def base_to_int(digits, b):
    n = 0
    c = 1
    for d in digits:
        n += c * d
        c *= b
    return n


lf3r = LF3R(n, seed, MASK)

# discard 2048 bytes
[lf3r() for _ in range(2048)]

flag_digits = []
for i in range(2048, len(stream)):
    flag_digits.append((stream[i] + 2 * lf3r()) % 3)
flag_int = base_to_int(flag_digits, 3)
flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, "big")
print(f"{flag = }")