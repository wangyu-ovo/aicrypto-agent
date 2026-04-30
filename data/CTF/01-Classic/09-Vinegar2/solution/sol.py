alphanumerical = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(){}_?'
matrix = []
for i in alphanumerical:
	matrix.append([i])

idx=0
for i in alphanumerical:
	matrix[idx][0] = (alphanumerical[idx:len(alphanumerical)]+alphanumerical[0:idx])
	idx += 1

ciphertext='*fa4Q(}$ryHGswGPYhOC{C{1)&_vOpHpc2r0({'
key='5up3r_s3cr3t_k3y_f0r_1337h4x0rs_r1gh7?'
flag=''
assert len(key)==len(ciphertext)
cipher_arr = []
key_arr = []
flag_arr=[]
for y in ciphertext:
	for i in range(len(alphanumerical)):
		if matrix[i][0][0]==y:
			cipher_arr.append(i)

for y in key:
	for i in range(len(alphanumerical)):
		if matrix[i][0][0]==y:
			key_arr.append(i)

for i in range(len(ciphertext)):
	flag_arr.append(cipher_arr[i]-key_arr[i])

for i in flag_arr:
	flag+=matrix[i][0][0]

print(flag)
