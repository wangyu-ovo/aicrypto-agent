from Crypto.Util.number import *
import os, hashlib
from secret import flag

def getrandbits(nbits):
    return bytes_to_long(os.urandom(nbits // 8))

p = getPrime(512)
while not isPrime(p//2):
    p = getPrime(512)

x = getrandbits(256)
y = pow(9,x,p)
enc = bytes([i^j for (i,j) in zip(flag, hashlib.sha384(long_to_bytes(x)).digest())])

f = open("output.txt","w")

f.write('p = ' + str(p) + '\n')
f.write('y = ' + str(y) + '\n')
f.write('enc = ' + enc.hex() + '\n')

for i in range(256):
    k = getrandbits(256)
    c = pow(9,x^k,p)
    f.write(str(k) + ' ' + str(c) + '\n')
    
