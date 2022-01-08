import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall('Hello, world'.encode())
    while True:
        data = s.recv(1024).decode()
        print(data)
        if data =='Success':
            s.close()
            break

print('Received', repr(data))