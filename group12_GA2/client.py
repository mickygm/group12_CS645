import socket

host = input("Type the User A's IP address: ")  
port = 12345        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((host, port))
    print("Connected to User A.")
    while True:
        message = c.recv(1024).decode()  
        print(f"User A: {message}")
        reply = input("User B: ")  
        c.sendall(reply.encode())  