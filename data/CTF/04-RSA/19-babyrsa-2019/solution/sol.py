#coding:utf8
import binascii,gmpy2
from helper import *
from functools import reduce
# from data import e1,e2,p,q1p,q1q,hint,flag,q2

n =  ns
c = cs


def CRT(mi, ai):
    assert(reduce(gmpy2.gcd,mi)==1)
    assert (isinstance(mi, list) and isinstance(ai, list))
    M = reduce(lambda x, y: x * y, mi)
    ai_ti_Mi = [a * (M // m) * gmpy2.invert(M // m, m) for (m, a) in zip(mi, ai)]
    return reduce(lambda x, y: x + y, ai_ti_Mi) % M

p=gmpy2.iroot(CRT(n, c), 4)[0]
print("p = ",p)
# ====================got p
n = n2
for i in range(200000):
	if gmpy2.iroot(ce1+n*i,42)[1]==1:
		res=gmpy2.iroot(ce1+n*i,42)[0]
		e1=res
		break

for i in range(200000):
	if gmpy2.iroot(ce2+n*i,3)[1]==1:
		res=gmpy2.iroot(ce2+n*i,3)[0]
		e2=res-tmp
		break
print("e1 = ",e1)
print("e2 = ",e2)
# ====================got e1,e2
e = e3
n = n3
c = c3

# yafu got q1p,q1q
q1p = 127587319253436643569312142058559706815497211661083866592534217079310497260365307426095661281103710042392775453866174657404985539066741684196020137840472950102380232067786400322600902938984916355631714439668326671310160916766472897536055371474076089779472372913037040153356437528808922911484049460342088835693
q1q = 127587319253436643569312142058559706815497211661083866592534217079310497260365307426095661281103710042392775453866174657404985539066741684196020137840472950102380232067786400322600902938984916355631714439668326671310160916766472897536055371474076089779472372913037040153356437528808922911484049460342088834871
if q1p>q1q:
	q1p,q1q=q1q,q1p

# below is not necessary
phi=(q1p-1)*(q1q-1)
assert(gmpy2.gcd(e,phi)==1)
d=gmpy2.invert(e,phi)
hint=pow(c,d,n)
hint=binascii.unhexlify(hex(hint)[2:])
print("hint = ",hint)
# ====================got  q1p as q1
# flag=int(binascii.hexlify(flag),16)
q1=q1p
print("q1 = ",q1)
assert(14==gmpy2.gcd(e1,(p-1)*(q1-1)))
assert(14== gmpy2.gcd(e2,(p-1)*(q2-1)))
e1=e1//14;e2=e2//14
n1=p*q1;n2=p*q2
phi1=(p-1)*(q1-1);phi2=(p-1)*(q2-1)
d1=gmpy2.invert(e1,phi1);d2=gmpy2.invert(e2,phi2)
f1=pow(c1,d1,n1);f2=pow(c2,d2,n2)

def GCRT(mi, ai):
    assert (isinstance(mi, list) and isinstance(ai, list))
    curm, cura = mi[0], ai[0]
    for (m, a) in zip(mi[1:], ai[1:]):
        d = gmpy2.gcd(curm, m)
        c = a - cura
        assert (c % d == 0)
        K = c // d * gmpy2.invert(curm // d, m // d)
        cura += curm * K
        curm = curm * m // d
        cura %= curm
    return (cura % curm, curm)

f3,lcm = GCRT([n1,n2],[f1,f2])
assert(f3%n1==f1);assert(f3%n2==f2);assert(lcm==q1*q2*p)
n3=q1*q2
c3=f3%n3
phi3=(q1-1)*(q2-1)
assert(gmpy2.gcd(7,phi3)==1)
d3=gmpy2.invert(7,phi3)
m3=pow(c3,d3,n3)
if gmpy2.iroot(m3,2)[1] == 1:
    flag=gmpy2.iroot(m3,2)[0]
    print(binascii.unhexlify(hex(flag)[2:]))
