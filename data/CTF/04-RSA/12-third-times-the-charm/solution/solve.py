from sympy.ntheory.modular import solve_congruence
from sympy import cbrt
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1337))
data = [int(x.split(b' ')[1]) for x in s.recv(4096).split(b'\n') if x != b'']

example_pairs = [(x, y) for x, y in zip(data[::2], data[1::2])]

# Apply the Chinese Remainder Theorem
M, _ = solve_congruence(*example_pairs)
# Compute the cube root of M (doesn't require any modular arithmetic)
plaintext_int = int(cbrt(M))
# Convert the integer back to bytes (assuming it's properly padded/formatted)
FLAG = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big').decode()

print(f'Recovered FLAG: {FLAG}')

