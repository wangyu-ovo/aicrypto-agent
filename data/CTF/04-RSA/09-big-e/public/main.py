from Crypto.Util.number import bytes_to_long, getPrime

flag = REDACTED

pt = bytes_to_long(flag)

p = getPrime(1024)
q = getPrime(1024)
n = p*q

e_1 = getPrime(16)
e_2 = getPrime(16)



ct_1 = pow(pt, e_1, n)
ct_2 = pow(pt, e_2, n)
print("ct_1 = ", ct_1)
print("ct_2 = ", ct_2)

print("e_1 = ", e_1)
print("e_2 = ", e_2)

print("n = ", n)

# 