from pwn import *
from Crypto.Util.number import *
import re


class Gao:
    def __init__(self):
        self.patt = r'(.+?)-bit'
        self.conn = remote('127.0.0.1', 1337)
    
    def gao_1(self):
        self.conn.recvuntil('send your')
        s = self.conn.recvline().decode()
        mat = re.search(self.patt, s)
        pbits = int(mat.group(1))
        while True:
            p = getPrime(pbits)
            if p % 4 == 1:
                k = p // 4
                break
        x, y = 2 * k + 1, k
        self.conn.sendline(f'{p}')
        self.conn.sendline(f'{x},{y}')
    
    def gao(self):
        for i in range(20):
            self.gao_1()
        self.conn.interactive()

if __name__ == '__main__':
    g = Gao()
    g.gao()