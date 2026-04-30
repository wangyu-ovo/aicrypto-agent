from pwn import *
def flip(a):
   return int(bin(a)[2:].zfill(128)[::-1], 2)
def gf2_128_mult(x, y):
    assert x < (1 << 128)
    assert y < (1 << 128)
    res = 0
    for i in range(127, -1, -1):
        res ^= x * ((y >> i) & 1)  # branchless
        x = (x >> 1) ^ ((x & 1) * 0xE1000000000000000000000000000000)
    assert res < 1 << 128
    return res

def gf_degree(a) :
  res = 0
  a >>= 1
  while (a != 0) :
    a >>= 1;
    res += 1;
  return res

def gf_invert(a, mod=340282366920938463463374607431768211591) :
  v = mod
  g1 = 1
  g2 = 0
  j = gf_degree(a) - 128

  while (a != 1) :
    if (j < 0) :
      a, v = v, a
      g1, g2 = g2, g1
      j = -j

    a ^= v << j
    g1 ^= g2 << j

    a %= 2**128  # Emulating 8-bit overflow
    g1 %= 2**128 # Emulating 8-bit overflow

    j = gf_degree(a) - gf_degree(v)

  return g1
def get_inverse(a):
   f = flip(a)
   inv = gf_invert(f)
   back = flip(inv)
   return back
aid = b"0"*32
mid = b"80"+b"0"*30
print(gf2_128_mult(2, 1 << 127))
conn = remote("127.0.0.1", 1337)

print(conn.recvline().decode())

print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(aid)
print(conn.recvline().decode())
tag1 = conn.recvline().decode().split(" = ")[1]
print(tag1)


print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(mid)
print(conn.recvline().decode())
tag2 = conn.recvline().decode().split(" = ")[1]
print(tag2)

print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(b"2")
print(conn.recvuntil(b">").decode())
conn.sendline(aid)
print(conn.recvline().decode())
tag3 = conn.recvline().decode().split(" = ")[1]
print(tag3)

print(conn.recvuntil(b">").decode())
conn.sendline(b"1")
print(conn.recvuntil(b">").decode())
conn.sendline(b"2")
print(conn.recvuntil(b">").decode())
conn.sendline(mid)
print(conn.recvline().decode())
tag4 = conn.recvline().decode().split(" = ")[1]
print(tag4)

H12 = int(tag2, 16) ^ int(tag1, 16)

H22 = int(tag4, 16) ^ int(tag3, 16)

target = int(tag1, 16) ^ int(tag3, 16)

inv = get_inverse(H12 ^ H22)

ta = gf2_128_mult(target, inv)
ans = hex(int(bin(ta)[2:].zfill(128),2))[2:]

print(conn.recvuntil(b">").decode())
conn.sendline(b"2")
print(conn.recvuntil(b">").decode())
conn.sendline(ans.encode())
conn.recvline()
print(conn.recvline())