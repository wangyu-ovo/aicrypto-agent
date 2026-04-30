import gensafeprime
from Crypto.Util.number import isPrime


ij = 1

def generate_safe_prime():
    global ij
    while True:
        ij += 1
        q = gensafeprime.generate(1024)
        if isPrime(2 * q + 1):
            return q
        print(f"Try: {ij}")

# Generate the first safe prime
q1 = generate_safe_prime()
print(f"First safe prime q1: {q1}")

# Generate the second safe prime
q2 = generate_safe_prime()
print(f"Second safe prime q2: {q2}")