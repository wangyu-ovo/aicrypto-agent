from Crypto.Util.number import bytes_to_long
import random
load('./helper.sage')

ec = EllipticCurve(Zmod(p**4),[a,b])
P = ec.point((X,Y,Z))

ec0 = EllipticCurve(Zmod(p),[a,b])
assert (n*p**3+241421)*P == 241421*P

# (target - m0*P)*(p**2)
P3 = (p**3+1)*P
diff = ZZ(P3[0]-P[0])
assert diff % (p**3) == 0
diff //= p**3

T1 = (P+(p**2+1)*target-(p**2-1)*m0*P)-target-m0*P # P + m1*p**3*P
m1 = (ZZ(T1[0]-P[0]) // (p**3))*inverse_mod(diff,p)%p
# (target - m0*P - m1*p*P)*p
T2 = P+(p+1)*target-target-(p-1)*(m0+m1*p)*P-(m0+m1*p)*P
m2 = (ZZ(T2[0]-P[0]) // (p**3))*inverse_mod(diff,p)%p
m02 = m0 + m1*p + m2*p**2

# (target - m02*P)
T3 = P+target-m02*P
assert ZZ(T3[0]-P[0]) % (p**3)==0
m3 = (ZZ(T3[0]-P[0]) // (p**3))*inverse_mod(diff,p)%p
m = m02 + m3*p**3

print(bytes.fromhex(hex(m)[2:]))