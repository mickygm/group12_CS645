import socket
import ascon

IP = input("Enter server IP: ")
port = 12345

#SHARED SECRETS
KEY = b'SECRETKEY1234567'
NONCE = b"\x00" * 16
ASSOCIATED_DATA = b"CS645/745 Modern Cryptography: Secure Messaging"

def encrypt_message(plaintext):
    return ascon.encrypt(key=KEY, nonce=NONCE, associateddata=ASSOCIATED_DATA,
                        plaintext=plaintext.encode(), variant="Ascon-128")

def decrypt_message(ciphertext):
    return ascon.decrypt(key=KEY, nonce=NONCE, associateddata=ASSOCIATED_DATA, 
                        ciphertext=ciphertext, variant="Ascon-128").decode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((IP, port))
    print("Connected to User B.")
    while True:
        message = input("User A: ")
        client_socket.sendall(encrypt_message(message))
        if message.lower() == 'exit':
            break
        encrypted_msg = client_socket.recv(1024)
        decrypted_message = decrypt_message(encrypted_msg)
        print("User B: ", decrypted_message)

print("Connection ended")