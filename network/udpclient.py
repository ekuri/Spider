import socket

udpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
target = ('127.0.0.1', 5555)

for data in ['Michael', 'Tracy', 'Sarah']:
	udpclient.sendto(data, target)
	d, addr = udpclient.recvfrom(1024)
	print d
	
udpclient.close()
