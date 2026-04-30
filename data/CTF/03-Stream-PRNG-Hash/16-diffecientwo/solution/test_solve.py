import pwn

proc = pwn.remote("127.0.0.1", 1337)

with open("found_keys.txt", "rb") as f:
    hashes = f.read().strip().split()

for h in hashes:
    proc.sendline(b'2')
    proc.sendline(h)

proc.sendline(b'3')
proc.interactive()
