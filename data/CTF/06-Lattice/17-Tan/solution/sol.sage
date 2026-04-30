bits = 1024
load('./helper.sage')
t = tan_flag
at = arctan(t)
pin = pi.n(bits)

L = matrix(QQ, [[1, 0, 0], [at, 1, at], [pin, 0, pin]])
L[:, 0] *= 2**bits
L = L.LLL()
L[:, 0] /= 2**bits
print(L[0])
m = abs(round(L[0][-1]))
print(m)
print(tan(m).n(bits))
print(t)
print(int(m).to_bytes((m.bit_length() + 7) // 8, "big"))
