import os

from pwn import remote
from tqdm import tqdm


p = 2**2281-1
partial_order = prod([3^2, 5^2, 7, 11, 13, 17, 31, 41, 61, 151, 191, 229, 241, 331, 457, 571, 761, 1217, 1321, 2281, 4561, 32377, 54721, 61681, 90289, 131101, 148961, 160969, 174763, 185821, 247381, 524287, 525313, 1101811, 1212847, 160465489, 420778751, 3996146881, 4562284561, 9036489073])
assert (p - 1) % partial_order == 0
assert partial_order >= 2**512


def bsgs(g, h, n, func_op, func_pow, func_inv, func_hash):
    """return x s.t. g^x = h"""
    m = ceil(sqrt(n))
    table = {}
    tmp = func_pow(g, 0)
    j = 0
    for j in range(m):
        table[func_hash(tmp)] = j
        tmp = func_op(tmp, g)
    factor = func_pow(func_inv(g), m)
    gamma = h
    for i in range(m):
        if func_hash(gamma) in table:
            j = table[func_hash(gamma)]
            ret = i * m + j
            assert func_pow(g, ret) == h
            return ret
        gamma = func_op(gamma, factor)


def pohlig_hellman(g, h, partial_order, func_op, func_pow, func_inv, func_hash):
    a_list = []
    b_list = []
    order = (p - 1) // 2
    for pi, e in list(factor(partial_order)):
        gi = func_pow(g, order // pi ** e)
        hi = func_pow(h, order // pi ** e)
        gamma = func_pow(gi, pi ** (e - 1))
        xk = 0
        for k in range(e):
            hk = func_pow(func_op(func_pow(func_inv(gi), xk), hi), (pi ** (e - 1 - k)))
            dk = bsgs(gamma, hk, pi, func_op, func_pow, func_inv, func_hash)
            xk = xk + pi ** k * dk
        xi = xk
        a_list.append(xi)
        b_list.append(pi ^ e)
    return crt(a_list, b_list)


if __name__ == "__main__":
    io = remote("127.0.0.1", int(1337))
    io.sendlineafter(b"> ", hex(p).encode())
    # The order of g is 4562
    g = p // 2
    # The order of h is (p - 1) // 2
    h = p // 3
    _ = io.recvuntil(b"r = ")
    r = int(io.recvline())

    func_op = lambda x, y: x * y % p
    func_pow = lambda x, y: pow(x, y, p)
    func_inv = lambda x: pow(x, -1, p)
    func_hash = lambda x: x

    for y in tqdm(range(4562)):
        t = (r - pow(g, y, p)) % p

        # Before full Pohlig Hellman for h^x = t, only mod 2281 is calculated and then check if y = xi mod 2281
        try:
            order = (p - 1) // 2
            xi = pohlig_hellman(h, t, 2281, func_op, func_pow, func_inv, func_hash)
        except TypeError:
            continue
        if xi != y % 2281:
            continue

        # Then full Pohlig Hellman
        try:
            res = pohlig_hellman(h, t, partial_order, func_op, func_pow, func_inv, func_hash)
        except TypeError:
            continue

        if res.nbits() <= 512:
            io.sendlineafter("x > ", str(res).encode())
            break
    else:
        print("not found")
        io.close()
        exit()

    print(io.recvline().strip().decode())