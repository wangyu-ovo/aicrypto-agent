import gmpy2
from helper import *

def continuedFra(x, y): 		#不断生成连分数的项,如127/52 = 2 + 1/2+ 1/3+ 1/1+ 1/5，生成[2,2,3,1,5]
    cF = []
    while y:
        cF += [x // y]
        x, y = y, x % y		#这里是连分数生成项的算法
    return cF

def Simplify(ctnf): 			#对前面生成的连分数项化简
    numerator = 1
    denominator = 0
    for x in ctnf[::-1]: 		#注意这里是倒叙遍历，从后面把连分数项合成总和。
        numerator, denominator = x * numerator + denominator, numerator 
    return (numerator, denominator) 		#把连分数分成和算出来的分母以元组的形式导出来，如Simplify(continuedFra(127,52))生成(127, 52)

def getit(c):
    cf=[]
    for i in range(1,len(c)):
        cf.append(Simplify(c[:i])) 	#各个阶段的连分数的分子和分母
    return cf 							#得到一串连分数，如：[(2, 1), (5, 2), (17, 7), (22, 9)]

def wienerAttack(e, n):				#低解密指数攻击，自己修改要碰撞的分子或分母
    cf=continuedFra(e,n)
    for (Q1,Q2) in getit(cf):			#遍历得到的连分数，令分子分母分别是Q1，Q2，因为前面我们说了N1/N2=(p1/p2)**2 (q1/q2)
        if Q1 == 0:
            continue
        if N1%Q1==0 and Q1!=1:		#满足这个条件就找到Q1了，其实这里的Q2也是对的。
            return (Q1,Q2)
    print('没找到能覆盖的分子/分母')

Q1,Q2=wienerAttack(N1,N2)				#找出一个Q1,其实这里也可以找出Q2的，但处于p2=sympy.nextprime(p1)的限制，只能用p1求出p2，不能用p2求出p1

from Crypto.Util.number import *
P1=gmpy2.iroot(N1//Q1,2)[0]			
P2=gmpy2.next_prime(P1)				#p1对了，p2也会对

phi1=P1*(P1-1)*(Q1-1)					#求出phi1，也就是ψ(n1)
phi2=P2*(P2-1)*(Q2-1)					#求出phi2，也就是ψ(n2)
d1=gmpy2.invert(E1,phi1)				#逆模求d
d2=gmpy2.invert(E2,phi2)				#逆模求d
m1=long_to_bytes(gmpy2.powmod(c1,d1,N1))		#普通解密算法，但是要用将long型数转为字节型数据
m2=long_to_bytes(gmpy2.powmod(c2,d2,N2))		#普通解密算法，但是要用将long型数转为字节型数据
print((m1+m2))							#拼接flag字符。
