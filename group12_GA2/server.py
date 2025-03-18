import socket

host = '0.0.0.0'
port = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print("Waiting for a connection...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected to User B: {addr}")
        while True:
            message = input("User A: ")  
            conn.sendall(message.encode())  
            reply = conn.recv(1024).decode()  
            print(f"User B: {reply}")