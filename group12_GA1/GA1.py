# We Williams Beaumont, Hunter Forsythe, and McKinley Morris
# declare that We have completed this
# computer code in accordance with the UAB Academic Integrity
# Code and the UAB CS Honor Code. I/We have read the UAB
# Academic Integrity Code and understand that any breach of the
# Code may result in severe penalties.
# Student signature(s)/initials: MM
# Date: 2/23/2025

import os

#Caesar cipher encryption
def c_encrypt(plain_text, key):
    cipher_text = ""
    for i in range(len(plain_text)):
        P = ord(plain_text[i]) #P = ASCII code of plaintext char
        if 0x21 <= P <= 0x7E: #if char is within printable range
            C = ( (P - 32 + int(key)) % 96) + 32 #C = ASCII code of ciphertext char
            cipher_char = chr(C) #ASCII code C -> char
        else:
            cipher_char = plain_text[i] #copy without change
        cipher_text += cipher_char
    return cipher_text
    

#Caesar cipher decryption
def c_decrypt(cipher_text, key):
    plain_text = ""
    for i in range(len(cipher_text)):
        C = ord(cipher_text[i]) #C = ASCII code of cipher char
        if 0x21 <= C <= 0x7E: #if char is within printable range
            P = ( (C - 32 - int(key)) % 96) + 32 #P = ASCII code of plaintext char
            plain_char = chr(P) #ASCII code P -> char
        else:
            plain_char = cipher_text[i] #copy without change
        plain_text += plain_char
    return plain_text
        

file_path = input("Type the name of your file\n")
file = open(file_path, "r")
content = file.read()
key = input("Enter your key (integer)\n")
user_choice = int(input("Enter 1 for encryption\nEnter 2 for decryption\n"))
try:
    match user_choice:
        case 1:
            cipher_text = c_encrypt(content, key)
            with open("cipher_text.txt", "w") as cipher_file:
                    cipher_file.write(cipher_text)
        case 2:
            plain_text = c_decrypt(content, key)
            with open("plain_text.txt", "w") as plain_file:
                    plain_file.write(plain_text)
        case default:
            print("Invalid input")
except ValueError:
    print("Please enter a valid option")