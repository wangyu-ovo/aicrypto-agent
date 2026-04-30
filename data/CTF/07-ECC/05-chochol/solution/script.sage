load('./helper.sage')

Gpx, Gpy = Gp
Hpx, Hpy = Hp
Gqx, Gqy = Gq
Hqx, Hqy = Hq



A = Gpx**3*Hpx - Hpx**3*Gpx + Hpy**2*Gpx - Gpy**2*Hpx
p = 243678574849421895808521345944938402807
assert A % p == 0

# solve q
B = Gqx**3*Hqx - Hqx**3*Gqx + Hqy**2*Gqx - Gqy**2*Hqx
q = 278451262698064898668334196027031252819
assert B % q == 0

# solve a
a = (Gpy^2 - Gpx^3) * pow(Gpx, -1, p) % p

Ep = EllipticCurve(GF(p), [a, 0])
Eq = EllipticCurve(GF(q), [a, 0])
Gp = Ep(Gpx, Gpy)
Gq = Eq(Gqx, Gqy)
Hp = Ep(Hpx, Hpy)
Hq = Eq(Hqx, Hqy)

print(factor(Ep.order()))
print(factor(Eq.order()))
s = Gp.discrete_log(Hp)
print(f'{s = }')
assert Hp == s*Gp
print(Hq == s*Gq)

for k in range(1, 99999):
    ss = s + k*Gp.order()
    assert Hp == ss*Gp
    if Hq == ss*Gq:
        print(f'{k = }')
        break

print(gcd(ss, p-1), gcd(ss, q-1))
p_roots = mod(c, p).nth_root(ss, all=True)
q_roots = mod(c, q).nth_root(ss, all=True)
for pp in p_roots:
    for qq in q_roots:
        flag = crt([Integer(pp), Integer(qq)], [p,q])
        try:
            print(bytes.fromhex(f'{int(flag):02x}').decode())
        except:
            pass