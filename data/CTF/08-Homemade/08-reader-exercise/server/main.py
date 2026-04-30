from Crypto.Util.number import *
from Crypto.Random.random import *


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


def gen_pair(deg, mod):
    while True:
        r = pow(getPrime(10), (n - 1) // (deg * 4), n)
        if pow(r, deg * 2, n) != 1:
            break
    piq = Polynomial([1])
    p_iq = Polynomial([1])
    inverse_2 = Polynomial([pow(2, -1, mod)])
    p_sign = Polynomial([1]) if randint(0, 1) == 1 else Polynomial([mod - 1])
    q_sign = Polynomial([1]) if randint(0, 1) == 1 else Polynomial([mod - 1])
    u = [Polynomial([pow(r, 2 * k + 1, mod), 1]) for k in range(deg * 2)]
    choices = sample(u, deg)
    for factor in u:
        if factor in choices:
            piq = piq * factor
        else:
            p_iq = p_iq * factor
    return ((piq + p_iq) * p_sign * inverse_2) % mod, ((piq - p_iq) * q_sign * inverse_2 * Polynomial([pow(r, deg, mod)])) % mod


if __name__ == "__main__":
    FLAG = "UMASS{1n5p1r3d_6y_pu7n@m_b4_2007}"
    size = 500
    base = 16
    degree = 8
    print(f"Gimme a sec to generate the prime...")
    while True:
        n = getPrime(size)
        if n % (base * 2) == 1:
            break
    print(f"n = {n}")

    p, q = gen_pair(degree, n)

    assert isinstance(p, Polynomial) and isinstance(q, Polynomial)
    assert p.degree() == degree
    assert q.degree() < p.degree()

    p_squared = p * p
    q_squared = q * q
    while True:
        decision = input("What would you like to do?\n")
        if decision == "challenge":
            challenge = int(input("I will never fail your challenges!\n"))
            proof = (p_squared(challenge) + q_squared(challenge)) % n
            assert proof == (pow(challenge, base, n) + 1) % n
            print(f"See? {proof}")
        elif decision == "verify":
            token = getRandomNBitInteger(size - 1) % n
            print("Here's how verification works: ")
            print(f"I give you:")
            print(f"token = {token}")
            print(f"You should give back:")
            print(f"p(token) = {p(token) % n}")
            print(f"q(token) = {q(token) % n}")

            print(f"Simple enough, right?")
            token = getRandomNBitInteger(size) % n
            print(f"token = {token}")
            p_attempt = int(input("p(token) = "))
            q_attempt = int(input("q(token) = "))
            assert p_attempt == p(token) % n and q_attempt == q(token) % n
            print("Great job!")
            print(FLAG)
            break
        else:
            print("Probably not that...")


