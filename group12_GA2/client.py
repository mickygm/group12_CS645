# We Williams Beaumont, Hunter Forsythe, and McKinley Morris
# declare that We have completed this
# computer code in accordance with the UAB Academic Integrity
# Code and the UAB CS Honor Code. I/We have read the UAB
# Academic Integrity Code and understand that any breach of the
# Code may result in severe penalties.
# Student signature(s)/initials: WAB, MM, HF
# Date: 3/21/2025

import socket
import ascon
import threading
import os

#Set target IP to User B's IP
IP = input("\nEnter server IP: ")
port = 12345

#SHARED SECRETS
KEY_AB = b'SECRETKEY1234567'
KEY_BA = b'SECRETKEY7654321'
NONCE = b"\x00" * 16
ASSOCIATED_DATA = b"CS645/745 Modern Cryptography: Secure Messaging"

#Encryption using Ascon
def encrypt_message(plaintext):
    return ascon.ascon_encrypt(key=KEY_AB, nonce=NONCE, associateddata=ASSOCIATED_DATA,
                        plaintext=plaintext.encode(), variant="Ascon-128")

#Decryption using Ascon
def decrypt_message(ciphertext):
    return ascon.ascon_decrypt(key=KEY_BA, nonce=NONCE, associateddata=ASSOCIATED_DATA, 
                        ciphertext=ciphertext, variant="Ascon-128").decode()

#Ends the connection between A and B by terminating the process on one end
def endConnection():
    print("\n<< Connection has been terminated. >>")
    os._exit(0)

#Sends messages from A to B
def send(socket):
    while True:
        message = "User A: " + input("")
        socket.sendall(encrypt_message(message))
        if message.lower() == 'user a: exit':
            endConnection()

#Receives messages from B to A
def receive(socket): 
    while True:
        encrypted_msg = socket.recv(4096)
        if not encrypted_msg:
            endConnection()
        decrypted_message = decrypt_message(encrypted_msg)
        print("   >>", decrypted_message)
        if decrypted_message.lower() == 'user b: exit':
            endConnection()

#Opens threads for sending and receiving messages at the same time
def chatOpen(socket):
    sendThread = threading.Thread(target = send, args = (socket,))
    receiveThread = threading.Thread(target = receive, args = (socket,))
    sendThread.start()
    receiveThread.start()
    sendThread.join()
    receiveThread.join()

#Establishes connection between A and B
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((IP, port))
    print("\n<< Connected to User B. When you are finished, type 'exit' to terminate the connection. >>\n")
    chatOpen(client_socket)