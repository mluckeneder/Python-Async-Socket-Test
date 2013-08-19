# Echo client program
import socket
for i in range(100):
	print("Iteration %i" % (i))
	HOST = 'localhost'    # The remote host
	PORT = 8080              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.send(b'Hello, world\n\r\n')
	data = b''
	with open("test.m4v", "wb") as f:
		while True:
			data = s.recv(4096)
			# print("recv")
			if not data:
				break

			f.write(data)


	s.close()


