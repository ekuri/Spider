import socket
import threading
import time

def tcplink(sock, addr, dealing):
    while True:
        data = sock.recv(1024)
        if dealing(data):
            break;
    sock.close()

def run(ip, port, maxconnection, dealing):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(maxconnection)
    print 'server listen at %s:%d' % ip % port

    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=tcplink, args=(sock, addr, dealing))
        t.start()

