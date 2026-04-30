#!/usr/bin/env sage
from secret import FLAG

assert FLAG.startswith(b"X-NUCA{") and FLAG.endswith(b"}")


def key_gen(bits):
    while True:
        p = random_prime(2 ** bits)
        q = random_prime(2 ** bits)
        if p % 4 == 3 and q % 4 == 3:
            break
    if p < q:
        p, q = q, p
    N = p * q
    while True:
        x = getrandbits(bits // 2)
        y = getrandbits(bits // 2)
        if gcd(x, y) == 1 and (x * y) < (int(sqrt(2 * N)) // 12):
            e = randint(int(((p + 1) * (q + 1) * 3 * (p + q) - (p - q) * int(N ** 0.21)) * y / (x * 3 * (p + q))),
                        int(((p + 1) * (q + 1) * 3 * (p + q) + (p - q) * int(N ** 0.21)) * y / (x * 3 * (p + q))))
            if gcd(e, (p + 1) * (q + 1)) == 1:
                k = inverse_mod(e, (p + 1) * (q + 1))
                break
    return (N, e, k)


if __name__ == "__main__":
    bits = 1024
    N, e, _ = key_gen(bits)

    pt = (int.from_bytes(FLAG[:32], 'big'), int.from_bytes(FLAG[32:], 'big'))
    ct = (0, 1)
    d = (((pt[1]) ** 2 - 1) * inverse_mod(((pt[1]) ** 2 + 1) * (pt[0]) ** 2, N)) % N

    # 2000 years later...:)
    for _ in range(e):
        ct = (int((ct[0] * pt[1] + ct[1] * pt[0]) * inverse_mod(1 + d * ct[0] * pt[0] * ct[1] * pt[1], N) % N),
              int((ct[1] * pt[1] + d * ct[0] * pt[0]) * inverse_mod(1 - d * ct[0] * pt[0] * ct[1] * pt[1], N) % N))

    f = open("output.txt", "wb")
    f.write(str((e, N)).encode() + b'\n')
    f.write(str(ct).encode())
    f.close()