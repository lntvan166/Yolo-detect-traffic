import socket
import time
import threading


def checkPortIsOpen(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    isOpen = False

    if result_of_check == 0:
        isOpen = True
    else:
        isOpen = False

    a_socket.close()

    return isOpen


def interruptListen(s):
    while True:
        print('check port 3000')
        if checkPortIsOpen(3000):
            time.sleep(10)
            continue
        else:
            print('app not work')
            s.close()
            break



def runServer(s):
    try:
        while True:
            print('listen')
            try:
                conn, addr = s.accept()
                if conn:
                    print('Connected by', addr)
                    data = conn.recv(1024).decode()
                    print('received {!r}'.format(data))
                    if not data:
                        break
                    if data == 'Close':
                        print('end')
                        break
                    time.sleep(5)
                    reply = 'Success'
                    conn.send(reply.encode())
            finally:
                break

    finally:
        s.close()

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1234  # Port to listen on (non-privileged ports are > 1023)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if s:
    s.bind((HOST, PORT))
    s.listen()
    threadCheckPort = threading.Thread(target=interruptListen, args=(s,))
    threadServer = threading.Thread(target=runServer, args=(s,))
    threadCheckPort.start()
    threadServer.start()
