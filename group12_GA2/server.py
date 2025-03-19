import socket
import ascon

IP = '' #WILL LISTEN TO ANY DEVICE ON THE NETWORK
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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP, port))
    s.listen()
    print("Connecting...")
    conn, addr = s.accept()
    print("Connected to User A:", addr)
    while True:
        encrypted_msg = conn.recv(1024)
        decrypted_msg = decrypt_message(encrypted_msg)
        print("User A:", decrypted_msg)
        message = input("User B: ")
        conn.sendall(encrypt_message(message))
        if message.lower() == 'exit':
            break

print("Connection ended")