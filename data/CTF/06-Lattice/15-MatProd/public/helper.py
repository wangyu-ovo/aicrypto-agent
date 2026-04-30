from sage.all import *


data = load('public/output.sobj')
challenges = data['challenges']
enc_flag = data['enc_flag']
nonce = data['nonce']