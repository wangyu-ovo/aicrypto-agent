#https://ctftime.org/writeup/33963

from Crypto.Util.number import *
import codecs
import string
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import itertools

def compositeModulusGCD(a, b):
    if(b == 0):
            return a.monic()
    else:
            return compositeModulusGCD(b, a % b)

def FranklinReiter(n, e, c1, c2, b):
    P.<x> = PolynomialRing(Zmod(n))
    f = (x)^e - c1
    g = (x+b)^e - c2
    m =  Integer(n-(compositeModulusGCD(f,g)).coefficients()[0])
    return m

def decrypt_flag(c,k):
    key = hashlib.sha256(k).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    print(cipher.decrypt(c))


from helper import *
elements = [13, -13]
coeffs = []
combinations_gen = itertools.product(elements, repeat=10)

encyprted_flag =  b"\xdb'\x0bL\x0f\xca\x16\xf5\x17>\xad\xfc\xe2\x10$(DVsDS~\xd3v\xe2\x86T\xb1{xL\xe53s\x90\x14\xfd\xe7\xdb\xddf\x1fx\xa3\xfc3\xcb\xb5~\x01\x9c\x91w\xa6\x03\x80&\xdb\x19xu\xedh\xe4"

for combo in combinations_gen:
    
    for c in combo:
        coeffs.append(c)

    a1 = coeffs[0] << 72
    a2 = coeffs[1] << 64
    a3 = coeffs[2] << 56
    a4 = coeffs[3] << 48
    a5 = coeffs[4] << 40
    a6 = coeffs[5] << 32
    a7 = coeffs[6] << 24
    a8 = coeffs[7] << 16
    a9 = coeffs[8] << 8
    a10 = coeffs[9]

    b = a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10
    
    candidate = long_to_bytes(FranklinReiter(n, e, c1, c2, b))

    coeffs = []

    try:
        key = candidate.decode()
        print("Found! :",key)
        decrypt_flag(encyprted_flag,key.encode())
        break
    except:
        continue