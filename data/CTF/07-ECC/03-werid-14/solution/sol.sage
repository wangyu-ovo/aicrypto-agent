def on_curve(C, P):
    a, d, p = C
    x, y = P
    return (a*x**2 + y**2 - d*x**2*y**2) % p == 1

def point_add(C, P, Q):
    a, d, p = C
    x1, y1 = P
    x2, y2 = Q
    assert on_curve(C, P) and on_curve(C, Q)
    x3 = (x1 * y2 + y1 * x2) * inverse_mod(1 + d * x1 * x2 * y1 * y2, p) % p
    y3 = (y1 * y2 - a * x1 * x2) * inverse_mod(1 - d * x1 * x2 * y1 * y2, p) % p
    return (int(x3), int(y3))

def point_mul(C, P, s):
    Q = (0, 1)
    while s > 0:
        if s % 2 == 1:
            Q = point_add(C, Q, P)
        P = point_add(C, P, P)
        s //= 2
    return Q

bits = 1024

'''
f = open('output.txt', 'rb').read()
data = f.replace(b'(', b'').replace(b')', b'').split(b'\n')

e, N = tuple(map(int, data[0].split(b', ')))
ct = tuple(map(int, data[1].split(b', ')))
'''
load('helper.sage')
res = [(i.denom(), i.numer()) for i in continued_fraction(e / N).convergents()]
P.<pp> = PolynomialRing(Zmod(N))

for x, y in res:
    if Integer(y).nbits() in range(bits // 2 - 8, bits // 2) and Integer(x).nbits() in range(bits // 2 - 8, bits // 2):
        U = (e * x // y) - N - 1
        V = int(sqrt(abs(U**2 - 4 * N)))
        p_0 = (U+V) // 2
        f = ((p_0 << 576) >> 576) + pp
        r = f.small_roots(X = 2**(bits - 576), beta = 0.4)
        if r != []:
            p = int(p_0 + r[0])
            if (N % p == 0) and is_prime(p):
                break

q = N // p
k = inverse_mod(e, (p + 1) * (q + 1))

d = (((ct[1])**2 - 1) * inverse_mod(((ct[1])**2 + 1) * (ct[0])**2, N)) % N
pt = point_mul((-d, d, N), ct, k)
flag = pt[0].to_bytes(32, 'big') + pt[1].to_bytes(32, 'big')
print(flag)