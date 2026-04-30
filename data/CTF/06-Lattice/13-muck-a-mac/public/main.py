import os
from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Util.strxor import strxor
from Crypto.Util.number import long_to_bytes, bytes_to_long
import string
import random
import secrets
import signal

signal.alarm(300)

def encrypt(key, aad, plaintext, nonce):
    cipher =  ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)
    ciphertext, mac = cipher.encrypt_and_digest(plaintext)
    return ciphertext, mac

class Challenge:
    def __init__(self):
        self.key = secrets.token_bytes(32)
        self.nonce = secrets.token_bytes(12)
        # debug

        self.plaintext = b""
        for i in range(4):
            self.plaintext += b"\x00"*13 + secrets.token_bytes(3)

        self.aad = b""
        for i in range(16):
            self.aad += bytes([random.choice(bytes(string.printable, 'ascii'))])
        

        self.is_get_ciphertext = False
        self.is_default = False
        self.is_change_aad = False
        self.is_xor_plaintext = False
        self.is_change_length = False
    
    def get_availables(self):
        res = ""
        if not self.is_get_ciphertext:
            res += f"[1]: get_ciphertext\n"
        if not self.is_default:
            res += f"[2]: default\n"
        if not self.is_change_aad:
            res += f"[3]: change_aad\n"
        if not self.is_xor_plaintext:
            res += f"[4]: xor_plaintext\n"
        if not self.is_change_length:
            res += f"[5]: change_length\n"
        res += f"[6]: answer\n"
        return res

    def get_ciphertext(self, plaintext):
        if self.is_get_ciphertext:
            return None
        self.is_get_ciphertext = True

        ciphertext, _ = encrypt(self.key, self.aad, plaintext, self.nonce)
        return ciphertext
    
    def default(self):
        if self.is_default:
            return None
        self.is_default = True

        _, mac = encrypt(self.key, self.aad, self.plaintext, self.nonce)
        return mac
    
    def change_aad(self, aad):
        if self.is_change_aad:
            return None
        self.is_change_aad = True
        _, mac = encrypt(self.key, aad, self.plaintext, self.nonce)
        return mac

    def xor_plaintext(self, target):
        if self.is_xor_plaintext:
            return None
        self.is_xor_plaintext = True
        _, mac = encrypt(self.key, self.aad, strxor(self.plaintext, target), self.nonce)
        return mac

    def change_length(self,l,r):
        if self.is_change_length or l < 0 or r < 0:
            return None
        self.is_change_length = True

        _, mac = encrypt(self.key, self.aad, self.plaintext[l:r], self.nonce)
        return mac

    def answer(self, ans):
        return self.plaintext == ans
        
def challenge():
    chal = Challenge()
    for count in range(6):
        print(chal.get_availables())
        menu = int(input("[menu]> "))

        if menu == 1:
            plaintext = b64decode(input("plaintext:"))
            print("(*'-') <", b64encode(chal.get_ciphertext(plaintext)).decode('utf-8'))
            pass

        if menu == 2:
            print("(*'-') < ", b64encode(chal.default()).decode('utf-8'))
            pass

        if menu == 3:
            aad = b64decode(input("aad:"))
            print("(*'-') <", b64encode(chal.change_aad(aad)).decode('utf-8'))
            pass

        if menu == 4:
            target = b64decode(input("target:"))
            print("(*'-') <", b64encode(chal.xor_plaintext(target)).decode('utf-8'))
            pass

        if menu == 5:
            l = int(input("l:"))
            r = int(input("r:"))
            print("(*'-') <", b64encode(chal.change_length(l,r)).decode('utf-8'))
            pass

        if menu == 6:
            answer = b64decode(input("answer:"))
            return chal.answer(answer)

success_cnt = 0
for i in range(100):
    if challenge():
        print(f"(*'-') <challenge{i} success")
        success_cnt += 1
    else:
        print("(*'-') <fail")
        break

if success_cnt == 100:
    print("(*'-') <perfect! here you are")
    flag = os.getenv("FLAG", "SECCON{dummyflagdummyflagdummyf}")
    print("(*'-') <flag is", flag)
