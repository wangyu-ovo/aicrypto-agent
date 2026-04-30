import os
m = 128
C = CyclotomicField(m)
F, PHI = C.maximal_totally_real_subfield()
zeta1280 = F.gen()
with open('public/pubkey_update') as f:
    fl = f.readlines()
    pk00, pk01 = eval(fl[0].strip().replace('^', '**'))
    pk10, pk11 = eval(fl[1].strip().replace('^', '**'))

pkey = matrix([[pk00, pk01], [pk10, pk11]])