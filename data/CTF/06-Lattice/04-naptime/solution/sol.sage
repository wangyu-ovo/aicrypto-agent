
def attack(ct, a):
    chunks = []
    for i in range(len(ct)):
        A = Matrix(ZZ, 9, 9,
             [
                 [1,0,0,0,0,0,0,0,a[0]],
                 [0,1,0,0,0,0,0,0,a[1]],
                 [0,0,1,0,0,0,0,0,a[2]],
                 [0,0,0,1,0,0,0,0,a[3]],
                 [0,0,0,0,1,0,0,0,a[4]],
                 [0,0,0,0,0,1,0,0,a[5]],
                 [0,0,0,0,0,0,1,0,a[6]],
                 [0,0,0,0,0,0,0,1,a[7]],
                 [0,0,0,0,0,0,0,0,-ct[i]]
             ]
                      )
        L = A.LLL()
        for row in L:
            if all(c == 0 or c == 1 for c in row):
                chunk = []
                for elem in row:
                    chunk.append(str(elem))
                chunks.append(chunk[:8])

    flag = "".join([chr(int("".join(chunk), base=2)) for chunk in chunks])
    print(f"CRACKED: {flag}")

def main():
    load('./helper.sage')
    attack(ct, a)

if __name__ == "__main__":
    main()
