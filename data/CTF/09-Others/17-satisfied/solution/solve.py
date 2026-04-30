from hamiltonicity import *
from pwn import *
import json

G = [
    [0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

perm = [0, 0, 1, 1, 2]
cycle = [(0, 2), (2, 1), (1, 4), (4, 3), (3, 0)]

# s = process(['python3', 'server.py'])
s = remote('127.0.0.1', 1337)
N = 5
A = permute_graph(G, N, perm)
numrounds = 128

s.sendlineafter(b"G:", json.dumps({"G": G}).encode())
A_, openings = commit_to_graph(A, N)

for r in range(numrounds):
    s.sendlineafter(b"send commitment A:", json.dumps({"A": A_}).encode())
    s.recvuntil(b"challenge bit is ")
    challenge = int(s.recvline())
    if challenge:
        o = get_r_vals(openings, N, cycle)
        z = [cycle, o]

    else:
        z = [perm, openings]

    s.sendlineafter(b"send proof z:", json.dumps({"z": z}).encode())

print(s.recvall().decode())