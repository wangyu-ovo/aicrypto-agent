from Crypto.Util.number import long_to_bytes

# killua4564 modify
def encrypt(m, b, g):
    c = 0
    for i in range(m):
        c += b * g / (n(pow(g, Rational(2*i/m)), prec = b) + g)
    return c

"""
encrypt ≈ m * b / (g + 1)

because c endswith .5, guess b = 2

(c * 2).factor() = 379 * 39719 * 8959787 * 891059823255825019255461632769683
because output.txt has 11955 percent digits, guess g + 1 = 39719

oops, there's the flag.
"""
load('./helper.sage')
flag = long_to_bytes(int(int(c * 2) / 39719)).decode()
print(f"CCTF{{{flag}}}")
