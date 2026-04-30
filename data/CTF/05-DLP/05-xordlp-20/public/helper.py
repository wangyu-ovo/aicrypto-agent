output = open('public/output.txt').read().split('\n')
p = int(output[0].split('= ')[1])
y = int(output[1].split('= ')[1])
enc = bytes.fromhex(output[2].split('= ')[1])
k, c = [], []
for i in output[3:-1]:
    k.append(int(i.split(' ')[0]))
    c.append(int(i.split(' ')[1]))

k = k

c = c
