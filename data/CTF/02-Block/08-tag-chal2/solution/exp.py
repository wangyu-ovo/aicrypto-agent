from pwn import *

INPUT1 = b"GET: flag.txt" + b"pad" # The last plaintext we send, is obligated start with this string to get the flag
INPUT2 = b"The-C0d3Bre4k3rs" # Second input, needs to be the same length as the first - 16 bytes
LEN16 = b'\x00' * 15 + b'\x10' # The length of our inputs

con = connect('127.0.0.1', 1337)

# con.recvuntil(b'disabled ==')
# con.recvline()

con.sendline(INPUT1)
con.sendline(b'irrelevant')
A = con.recvline()[:-1] # the output of INPUT1 + ITS_LEN

con.sendline(INPUT2)
con.sendline(b'irrelevant')
B = con.recvline()[:-1] # the output of INPUT2 + ITS_LEN

# The parts that make B then A
con.sendline(INPUT2 + LEN16 + A)
con.sendline(b'irrelevant')
result = con.recvline()[:-1]

# The parts that make A then B
con.sendline(INPUT1 + LEN16 + B)
con.sendline(result) # This has the same result as the one we performed above

flag = con.recvline()[:-1]
print(flag)

con.close()