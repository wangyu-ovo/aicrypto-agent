import os
with open('./pubkey_update') as f:
    fl = f.readlines()
    pk00, pk01 = eval(fl[0].strip().replace('^', '**'))
    pk10, pk11 = eval(fl[1].strip().replace('^', '**'))

pkey = matrix([[pk00, pk01], [pk10, pk11]])