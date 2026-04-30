import random
from Crypto.Util.number import getPrime
import secrets
from flag import flag

def get_Rrandom(R):
    return secrets.randbelow(int(R.order()))

def make_G(R, alphas):
    mat = []
    for i in range(k):
        row = []
        for j in range(n):
            row.append(alphas[j]^i)
        mat.append(row)
    mat = matrix(R, mat)
    return mat

def split_p(R, p, prime_bit_length, length):
    step = ceil(prime_bit_length/length)
    res = []
    while p > 0:
        res.append(ZZ(p % (2**step)))
        p >>= step
    return vector(R, res)

def make_random_vector(R, length):
    error_range = 2^1000
    res = []
    for _ in range(length):
        res.append(R(secrets.randbelow(int(error_range))))
    return vector(R, res)

def make_random_vector2(R, length):
    error_cnt = 28
    res = vector(R, length)
    error_pos = random.sample(range(length), error_cnt)
    for i in error_pos[:error_cnt//2]:
        res[i] = get_Rrandom(R)*p
    for i in error_pos[error_cnt//2:]:
        res[i] = get_Rrandom(R)*q
    return vector(R, res)

n, k = 36, 8
prime_bit_length = 512
p = getPrime(prime_bit_length)
q = getPrime(prime_bit_length)
N = p*q
R = Zmod(N)
alphas = vector(R, [get_Rrandom(R) for _ in range(n)])
G = make_G(R, alphas)
dets = [G.submatrix(0,i*k-i,8,8).det() for i in range(5)]
double_alphas = list(map(lambda x: x^2, alphas))
alpha_sum_rsa = R(sum(alphas))^65537

keyvec = vector(R, [get_Rrandom(R) for _ in range(k)])
pvec = split_p(R, p, prime_bit_length, k)

p_encoded = pvec*G + make_random_vector(R, n)
key_encoded = keyvec*G + make_random_vector2(R, n)

print(f"{N=}")
print(f"{dets=}")
print(f"{double_alphas=}")
print(f"{alpha_sum_rsa=}")
print(f"{p_encoded=}")
print(f"{key_encoded=}")

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
key = hashlib.sha256(str(keyvec).encode()).digest()
cipher = AES.new(key, AES.MODE_ECB)
encrypted_flag = cipher.encrypt(pad(flag, AES.block_size))
print(f"{encrypted_flag=}")
