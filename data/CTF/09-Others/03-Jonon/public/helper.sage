import os
filename = r'public/output.txt'

with open(filename) as f:
    s = f.read().splitlines()

pkey = '\n'.join(s[:157])[8:-1]
mat_list = pkey.split('], [')

def get_matrix(x):
    x_ = x.replace('[', '').replace(']', '')
    xlines = x_.splitlines()
    ret = [[int(xij) for xij in xline.strip().split()] for xline in xlines]
    return matrix(ZZ, ret)

mat_list = list(map(get_matrix, mat_list))
C = '\n'.join(s[157:162])[4:]
C = get_matrix(C)