from pwn import *
import hlextend

s = hlextend.new('sha1')

def main():
    p = remote('127.0.0.1', 1337)
    # print(p.recvline().decode('ascii')[:-1])

    message = 'GET FILE: '
    injection = 'flag.txt'

    original_tag = p.recvline().decode('ascii')[:-1]
    print(original_tag)

    new_message = s.extend(injection.encode(), message.encode(), 1200, original_tag)
    print(new_message)
    new_hash = s.hexdigest()
    print(new_hash)

    p.sendline(new_message)
    p.sendline(new_hash.encode())
    print(p.recvuntil('}'))

main()