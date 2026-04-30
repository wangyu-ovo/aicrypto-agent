def decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha(): 
            shifted = ord(char) - shift
            if char.islower(): 
                if shifted < ord('a'):
                    shifted += 26
            elif char.isupper(): 
                if shifted < ord('A'):
                    shifted += 26
            decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text


import os

with open(r"./cipher.txt", 'r') as file:
    encrypted_text = file.read()

for shift in range(26):
    decrypted_text = decrypt(encrypted_text, shift)
    if "utflag" in decrypted_text:
        index_flag = decrypted_text.index('utflag')
        print(decrypted_text[index_flag:index_flag+17])
