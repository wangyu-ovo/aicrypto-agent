from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from Crypto.Util.strxor import strxor
import os
import signal

FLAG = os.getenv('FLAG', 'SECCON{dummy}')

chunk_size = 5


def gen_key():
    p = getPrime(64)
    r = bytes_to_long(os.urandom(8))
    H = os.urandom(5)
    pub = p
    priv = (p, r, H)
    return pub, priv


def encrypt(message, priv):
    p, r, H = priv
    assert len(message) % 5 == 0

    message_chunks = [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]

    ciphertext = b""
    mac = 0
    for chunk in message_chunks:
        temp = strxor(chunk, H)
        mac = (r * (mac + bytes_to_long(temp))) % p
        ciphertext += temp

    return ciphertext, long_to_bytes(mac)


def decrypt(ciphertext, mac, priv):
    mac = bytes_to_long(mac)
    p, r, H = priv
    ciphertext_chunks = [ciphertext[i:i + chunk_size] for i in range(0, len(ciphertext), chunk_size)]

    message = b""
    expected_mac = 0
    for chunk in ciphertext_chunks:
        expected_mac = (r * (expected_mac + bytes_to_long(chunk))) % p
        message += strxor(chunk, H)
    if mac == expected_mac:
        return message
    else:
        return None


def main():
    signal.alarm(120)
    p, priv = gen_key()
    print(f"{p=}")
    messages = []
    truncated_macs = []
    for i in range(42):
        message = os.urandom(5)
        _, mac = encrypt(message, priv)
        messages.append(message.hex())
        truncated_macs.append(mac[:-2].hex())
    print(f"{messages=}")
    print(f"{truncated_macs=}")

    c = bytes.fromhex(input("ciphertext:"))
    mac = bytes.fromhex(input("mac:"))
    return decrypt(c, mac, priv) == b"Kurenaif,gimme flag!"


if main():
    print(FLAG)