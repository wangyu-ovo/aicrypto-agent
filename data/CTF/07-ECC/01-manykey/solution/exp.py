from pwn import remote
from hashlib import sha1
from ecdsa import SigningKey, ellipticcurve, curves
from sympy import sqrt_mod

def lift_x(x, a, b, p):
    return sqrt_mod(x**3 + a*x + b, p)

io = remote("127.0.0.1", "21726")
io.recvuntil("Hello,")
msg = bytes.fromhex(io.recvline().decode().split()[-1])
h = int(sha1(msg).hexdigest(), 16)

sig = io.recvline().decode()
r = int(sig[:48], 16)
s = int(sig[48:], 16)
io.read()

def attack(h, r, s):
    # NIST192p params
    p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff
    a = 0xfffffffffffffffffffffffffffffffefffffffffffffffc
    b = 0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1
    n = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831
    curve = ellipticcurve.CurveFp(p, a, b)

    kG = ellipticcurve.PointJacobi(curve, x=r, y=lift_x(r, a, b, p), z=1, order=n)
    d = 42069 # choose whatever privkey your heart desires
    t = (s * pow(h+r*d, -1, n)) % n
    CG = t*kG
    mycurve = curves.Curve(curve=curve, generator=CG, oid=None, name="my curve xD")
    return SigningKey.from_secret_exponent(secexp=d, curve=mycurve).to_der().hex()

der = attack(h, r, s)
io.sendline(der.encode())
print(io.readline().decode())

# irisctf{key_generating_machine}