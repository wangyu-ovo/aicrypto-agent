from Crypto.Util.number import *
from helper import *


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
g, x, y = gcdExtended(e1, e2) 
print("gcd(", e1 , "," , e2, ") = ", g, "Where: x = ", x, " and y = ",y) 

# gcd( 71 , 101 ) =  1 Where: x =  37  and y =  -26

# As y is negative, we need to calculate the inverse of c2 :

import gmpy2  # You'll need to install the gmpy2 library

# Define the values

# Calculate the modular inverse
inverse_c2 = gmpy2.invert(c2, n)

if inverse_c2 is not None:
    print(f"The modular inverse of c2 modulo n is: {inverse_c2}")
else:
    print("The modular inverse does not exist for the given inputs.")

msg = (pow(c1,x) * pow(inverse_c2,(-y))) % n

print("Message: ", long_to_bytes(msg))
