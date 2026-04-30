from Crypto.Util.number import *
load('./helper.sage')
# S.<x> = R.quotient(N)
# factor(N)
q1, q2 = N.factor()
q1, q2 = q1[0], q2[0]

phi = (p2**q1.degree() - 1) * (p2**q2.degree() - 1)

e = 0x10001
d = inverse_mod(e, phi)
m = pow(c2,d,N)
h1 = list(m.coefficients(sparse=False))
h =int("".join([str(i) for i in h1]))
assert h<p1

M=matrix(ZZ,[
    [1,h],
    [0,p1]])
L=M.LLL()

from tqdm import tqdm
g_=abs(L[0,1])

for rand in tqdm(range(2^20)):
    g = g_^^rand
    if is_prime(g):
        if gcd(n,g)!=1:
            g,p=g,n//g
            print(f"[+] find {g,n//g}")
            break
phi=(p-1)*(g-1)
print(long_to_bytes(int(pow(c1,inverse(e,phi),p*g))))