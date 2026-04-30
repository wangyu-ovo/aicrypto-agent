from Crypto.Util.number import *
import random
from gmpy2 import *
from libnum import *
from flag import flag

def padding(f):
    random_chars = bytes([random.randint(0, 255) for _ in range(32)])
    f = f + random_chars
    return f

def guess_p(p):
    e = 65537
    
    P = p
    n1 = getPrime(512)*getPrime(512)
    with open('enc.txt', 'w+') as f:
        while jacobi(2,n1) == 1:
            n1 = getPrime(512)*getPrime(512)
        while P:
            pad = random.randint(0, 2**2023)**2 
            message = pad << 1 + P % 2
            cipher = pow(message, e, n1)
            f.write(str(cipher)+'n')
            P //= 2
    print("n1 = "+ str(n1) )    
    
def guess_q(q):
    
    def encrypt(q, n):
        e = random.randint(1000,2000)
        noise = random.randint(0, n - 1)
        c = pow(q+noise,e,n)
        return e, noise,c 
    
    n2 = getPrime(512)*getPrime(512)
    e1, noise1, c1 = encrypt(q, n2)
    e2, noise2, c2 = encrypt(q, n2)
    print("n2 = "+ str(n2) ) 
    print('(e1, noise1, c1) =', (e1,noise1,c1))
    print('(e2, noise2, c2) =', (e2,noise2,c2))
p = getPrime(512)
q = getPrime(512)

n = p*q
guess_p(p)
guess_q(q)
e = 0x10001
flag = padding(flag)
m = bytes_to_long(flag)
c = pow(m,e,n)

print("c = " + str(c))
'''
'''