def egcd(a, b):
    if a == 0:
        return 0, 1
    else:
        y, x = egcd(b % a, a)
        return x - (b // a) * y, y

# use yafu
from helper import *
p = 861346721469213227608792923571
q = 1157379696919172022755244871343
assert(p*q == n)

yp, yq = egcd(p, q)

def solve(i, c):
    if(i == 0):
        try:
            print(bytearray.fromhex(hex(c)[2:]).decode())
            return
        except:
            None
        return
    mp = pow(c, (p+1)//4, p)
    mq = pow(c, (q+1)//4, q)
    r1 = (yp*p*mq + yq*q*mp)%n
    r2 = n-r1
    r3 = (yp*p*mq-yq*q*mp)%n
    r4 = n-r3
    solve(i-1, r1)
    solve(i-1, r2)
    solve(i-1, r3)
    solve(i-1, r4)

solve(16, c)
