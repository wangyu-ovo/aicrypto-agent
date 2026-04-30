from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
with open('key', 'wb') as f:
    f.write(key)
