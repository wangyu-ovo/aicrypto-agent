from Crypto.Util.number import *
from pwn import *


class Polynomial:
    def __init__(self, entries):
        self.entries = entries

    def __add__(self, other):
        if len(self.entries) < len(other.entries):
            return other + self
        return Polynomial(
            [x if y == 0 else (y if x == 0 else x + y) for x, y in zip(self.entries, other.entries)] +
            self.entries[len(other.entries):]
        )

    def __neg__(self):
        return Polynomial([-x for x in self.entries])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, o):
        result = Polynomial([])
        for power in range(len(self.entries)):
            product = [0] * power + [self.entries[power] * y for y in o.entries]
            result = result + Polynomial(product)
        return result

    def __mod__(self, other):
        self.entries = [x % other for x in self.entries]
        return self

    def __str__(self):
        return str(self.entries)

    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs):
        start = 1
        s = self.entries[0]
        for i in self.entries[1:]:
            start *= args[0]
            s += i * start
        return s

    def degree(self):
        i = len(self.entries)
        while i > 0:
            i -= 1
            if self.entries[i] != 0:
                break
        return i

io = remote('127.0.0.1', 34542)
io.recvuntil('n = ')
n = int(io.recvline())
io.recvuntil('What would you like to do?')
io.sendline('verify')
io.recvuntil('token = ')
token = int(io.recvline())
io.recvuntil('p(token) = ')
p_token = int(io.recvline())
io.recvuntil('q(token) = ')
q_token = int(io.recvline())

io.recvuntil('token = ')
given_token = int(io.recvline())

# Generate any 32nd root of unity modulo n
while True:
    r = pow(getPrime(10), (n - 1) // (8 * 4), n)
    if pow(r, 8 * 2, n) != 1:
        break
# Polynomials of the form (x - unity_root)
u = [Polynomial([pow(r, 2 * k + 1, n), 1]) for k in range(16)]
inverse_2 = Polynomial([pow(2, -1, n)])
negative_1 = Polynomial([n - 1])

# There should be a better of doing this, but I'm lazy and this works...
p_final = 0
q_final = 0
p_list = []
for i1 in range(0, 16):
    for i2 in range(0, i1):
        for i3 in range(0, i2):
            for i4 in range(0, i3):
                for i5 in range(0, i4):
                    for i6 in range(0, i5):
                        for i7 in range(0, i6):
                            for i8 in range(0, i7):
                                # all possible sets of 8 out of 16 factors
                                choice = [i8, i7, i6, i5, i4, i3, i2, i1]
                                piq = Polynomial([1])
                                p_iq = Polynomial([1])
                                for i in range(16):
                                    if i in choice:
                                        piq = piq * u[i]
                                    else:
                                        p_iq = p_iq * u[i]
                                p = ((piq + p_iq) * inverse_2) % n
                                q = ((piq - p_iq) * inverse_2 * Polynomial([pow(r, 8, n)])) % n
                                if p_token == p(token) % n:
                                    print(f"p = {p(given_token)}")
                                    if p_final == 0:
                                        p_final = p(given_token)
                                if q_token == q(token) % n:
                                    print(f"q = {q(given_token)}")
                                    if q_final == 0:
                                        q_final = q(given_token)
                                # # -p and p doesn't matter for p^2; same for q
                                if p_final != 0 and q_final != 0:
                                    print(p_final)
                                    print(q_final)
                                    print(p_token == p(token) % n)
                                    io.recvuntil('p(token) = ')
                                    io.sendline(str(p(given_token) % n))
                                    io.recvuntil('q(token) = ')
                                    io.sendline(str(q(given_token) % n))
                                    io.interactive()
