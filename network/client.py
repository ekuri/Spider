import socket

def run(ip, port, hello, dealing):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = (ip, port)
    s.connect(address)
    while True:
        s.send(hello)
        data = s.recv(1024)
        dealing(data)
    s.close()
    