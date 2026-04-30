from helper import *


def find_nexts(p_lsb, q_lsb):
    new_mod = mod * (2**16)
    pairs = []
    for p_s in p_splitted:
        for q_s in q_splitted:
            p_next = (p_lsb + p_s * mod)
            q_next = (q_lsb + q_s * mod)
            if (N - p_next * q_next) % new_mod == 0:
                print(p_s, q_s)
                pairs.append((p_s, q_s))
    return pairs

p_lsb = 0
q_lsb = 0
mod = 1
l = len(p_splitted)
for _ in range(l):
    pairs = find_nexts(p_lsb, q_lsb)
    print(pairs)
    assert len(pairs) > 0

    idx = 0
    if len(pairs) > 1 and pairs[1][0] == 44532:
        idx = 1
    p_lsb += pairs[idx][0] * mod
    q_lsb += pairs[idx][1] * mod
    mod *= 2**16
    p_splitted.remove(pairs[idx][0])
    q_splitted.remove(pairs[idx][1])
    
assert p_lsb * q_lsb == N

print(f'p = {p_lsb}')
print(f'q = {q_lsb}')

e = 0x10001
d = pow(e, -1, (p_lsb-1)*(q_lsb-1))
m = pow(c, d, N)
print(m.to_bytes((m.bit_length() + 7) // 8, 'big'))
