from Crypto.Util.number import inverse, isPrime
from pwn import *

io = remote('127.0.0.1', 1337)
io.recvuntil('MySeededHash(')
N = int(io.recvuntil(',')[:-1])
# Change your N value
e = 65537
first_block  = str("11" + " ") + str("00" + " ") * 127 + str("11" + ' ') * 128
second_block = str("11" + " ") * 128 + str("00" + ' ') * 127 + str("11" + " ")
third_block = str("00111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100")


int_first_block = int(first_block.replace(" ", ""), 16)
int_second_block = int(second_block.replace(" ", ""), 16)
int_third_block = int(third_block, 16)

def get_block_in_bytes(int_block):
    global N
    global e

    phi_N = N - 1  # Since N is a prime, phi(N) = N - 1
    d = inverse(e, phi_N)
    x = pow(int_block, d, N)
    x = x.to_bytes(256, "big")

    return x

def sep_bytes_in_block(bytes_block):
    bytes_block = bytes_block.hex()
    bytes_block_sep = ''

    for i in range(0, len(bytes_block), 2):
        bytes_block_sep += bytes_block[i:i+2] + ' '

    return bytes_block_sep


first_block_in_bytes = get_block_in_bytes(int_first_block)
second_block_in_bytes = get_block_in_bytes(int_second_block)
third_block_in_bytes = get_block_in_bytes(int_third_block)

sep_bytes_blocks = sep_bytes_in_block(first_block_in_bytes) + sep_bytes_in_block(second_block_in_bytes) + sep_bytes_in_block(third_block_in_bytes)

io.recvuntil('> ')
io.sendline(sep_bytes_blocks)
io.recvuntil('hash(input) ==')
io.sendline('0' * 256)
io.interactive()
