from Crypto.Util.number import getStrongPrime
from random import shuffle

flag = b'FAKE{THIS_IS_FAKE_FLAG}'


p = getStrongPrime(1024)
q = getStrongPrime(1024)

N = p * q
e = 0x10001
m = int.from_bytes(flag, 'big')
c = pow(m, e, N)


# "Aaaaargh!" -- A sharp, piercing scream shattered the silence.

p_bytes = p.to_bytes(128, 'big')
q_bytes = q.to_bytes(128, 'big')

fraction_size = 2
p_splitted = [int.from_bytes(p_bytes[i:i+fraction_size], 'big') for i in range(0, len(p_bytes), fraction_size)]
q_splitted = [int.from_bytes(q_bytes[i:i+fraction_size], 'big') for i in range(0, len(q_bytes), fraction_size)]

shuffle(p_splitted)
shuffle(q_splitted)


print(f'N = {N}')
print(f'c = {c}')
print(f'p_splitted = {p_splitted}')
print(f'q_splitted = {q_splitted}')
