from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

RUN_LOCALLY = True


def ROTL(a, b):
    return (((a) << (b)) | ((a % 2**32) >> (32 - (b)))) % 2**32

def qr(x, a, b, c, d):
    x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d],16)
    x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b],12)
    x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d], 8)
    x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b], 7)

ROUNDS = 20

def chacha_block(inp):
    x = list(inp)
    for i in range(0, ROUNDS, 2):
        qr(x, 0, 4, 8, 12)
        qr(x, 1, 5, 9, 13)
        qr(x, 2, 6, 10, 14)
        qr(x, 3, 7, 11, 15)

        qr(x, 0, 5, 10, 15)
        qr(x, 1, 6, 11, 12)
        qr(x, 2, 7, 8, 13)
        qr(x, 3, 4, 9, 14)

    return [(a+b) % 2**32 for a, b in zip(x, inp)]

def buffer_to_state(buffer):
    buffer_bytes = bytes.fromhex(buffer)
    output = []
    for i in range(0, len(buffer_bytes), 4):
        output.append(bytes_to_long(buffer_bytes[i:i+4]))
    return output

def find_flag(initial_state, encrypted_flag):
    buffer = b""
    state = chacha_block(initial_state)     # we have to start with this since we already used the first state with our initial input
    flag_bytes = bytes.fromhex(encrypted_flag)
    flag_length = len(flag_bytes)
    output = []
    for i in range(flag_length):
        if len(buffer) == 0:
            buffer = b"".join(long_to_bytes(x).rjust(4, b"\x00") for x in state)
            state = chacha_block(state)
        output.append(chr(flag_bytes[i] ^ buffer[0]))
        buffer = buffer[1:]
    return "".join(output)

def get_tube():
    p = None
    lines_to_skip = 4
    p = remote('127.0.0.1', 1337)
    for _ in range(lines_to_skip):
        p.recvline()
    return p

def get_buffer0(p):
    p.sendline(b'1')
    p.recvline()
    p.sendline(b'\x00'*64)
    return p.recvline()[4:-1].decode()

def get_encrypted_flag(p):
    p.sendline(b'2')
    return p.recvline()[2:-1].decode()

if __name__ == "__main__":
    p = get_tube()
    buffer0 = get_buffer0(p)
    initial_state = buffer_to_state(buffer0)
    encrypted_flag = get_encrypted_flag(p)
    print(find_flag(initial_state, encrypted_flag))