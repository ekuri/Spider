import socket
import threading
import time

udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsock.bind(('127.0.0.1', 5555))

while True:
	data, addr = udpsock.recvfrom(1024)
	print 'recv data: ' + data
	udpsock.sendto('server recv: ' + data, addr)
	
udpsock.close()