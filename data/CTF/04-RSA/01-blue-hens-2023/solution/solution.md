# RSA School 3rd Grade 

## Description

> Hope you paid attention in math class
>
> Textbook (optional): https://bitsdeep.com/posts/attacking-rsa-for-fun-and-ctf-points-part-1/

## Write-Up

In this scenario, we see that the message jas been encrypted with the same modulus but with different exponent.

We can use **Common modulus attack** to recover the flag.

First, by using **Extended Euclid’s Algorithm** and from **Bezout's Identity**, since `e1` and `e2` are prime between them, we recover the `u` and `v`, coefficients of the identity, which will help us get back the message.

```
gcd( 71 , 101 ) =  1 Where: x =  37  and y =  -26
```

As `y` is negative, we need to invert `c2`.

```
The modular inverse of c2 modulo n is: 54172700333672762288629604527455423922016596676982257395665328987119679698867011635703852807846208115145731488506455254374796653572209246934430604524661770729811520718292171255404216928716021422357220344808103594004420799169520844909546439199452837619270565298019757280857547201586228753025977302180211494855
```

Finally, we recover the message using the following equation:

```
msg = (pow(c1,x) * pow(inverse_c2,(-y))) % n
```

From there:

```
Message:  b'UDCTF{3uc1id_th4_60at}'
```

Full script:

```py
from Crypto.Util.number import *


def gcdExtended(a, b): 
    # Base Case 
    if a == 0 : 
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y 
     
 
# Driver code 
e1, e2 = 71, 101
g, x, y = gcdExtended(e1, e2) 
print("gcd(", e1 , "," , e2, ") = ", g, "Where: x = ", x, " and y = ",y) 

# gcd( 71 , 101 ) =  1 Where: x =  37  and y =  -26

# As y is negative, we need to calculate the inverse of c2 :

import gmpy2  # You'll need to install the gmpy2 library

# Define the values

c1 = 1421275848974615267320815554113040672023972283807752574007971561416386636110464890632994733734995114229161525885389065244354678964389211537085513310823751266472044865745324866096898051759507738772227296453397678055024824805366251635154522059070310922367078281343183508274450904681187384450253350434931649011
c2 = 26097095086985946477598349002260598942399303275420948828501512467473619292573670218058274201990116295246084096584962695127706609264424951086000719935218496250047555039460733768633688410770610612614744411304261153778159881980276162174277085197608466835857196307432992312260307797540746411319330318058866868362
n = 87587426608653108851564813489752475287019321764561555461700901651463446024854423042554629096780987943450742890279417241231211446818009232077230407281610183609540264821974669679932743621434901779832901512681108061652309435608446510337833028029876549629818957952682516026313018526405972829923620377438164377109  # Replace with your actual modulus value

# Calculate the modular inverse
inverse_c2 = gmpy2.invert(c2, n)

if inverse_c2 is not None:
    print(f"The modular inverse of c2 modulo n is: {inverse_c2}")
else:
    print("The modular inverse does not exist for the given inputs.")

msg = (pow(c1,x) * pow(inverse_c2,(-y))) % n

print("Message: ", long_to_bytes(msg))

```


## Flag

UDCTF{3uc1id_th4_60at}