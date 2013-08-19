# python -mtimeit -n1 -r2 'import client; client.test_client()'
# 1 loops, best of 2: 77.4 sec per loop
import socket
import select
import os

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
file_name = "../../Desktop/film.m4v"
file_size = os.path.getsize(file_name)
try:
	connections = {}
	requests = {}
	responses = {}
	response_file = {}
	while True:
		# print("Serving a request")

		events = epoll.poll(60)

		for fileno, event in events:
			if fileno == serversocket.fileno():
				conn, address = serversocket.accept()
				conn.setblocking(0)
				epoll.register(conn.fileno(), select.EPOLLIN)
				connections[conn.fileno()] = conn
				requests[conn.fileno()] = b''
				response_file[conn.fileno()] = (open(file_name, 'rb'), 0)

			elif event == select.EPOLLIN:
				requests[fileno] += connections[fileno].recv(1024)
				if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
					epoll.modify(fileno, select.EPOLLOUT)
					print('-'*40 + '\n' + requests[fileno].decode()[:-2])

			elif event == select.EPOLLOUT:
				f, p = response_file[fileno]
				byteswritten = os.sendfile(fileno, f.fileno(), p, 8192)
				 # = connections[fileno].send(f.read(8192))
				response_file[fileno] = (f, p+byteswritten)
				if p+byteswritten == file_size:
					epoll.modify(fileno, 0)
					connections[fileno].shutdown(socket.SHUT_RDWR)


			elif event & select.EPOLLHUP:
				epoll.unregister(fileno)
				connections[fileno].close()
				del connections[fileno]
				del response_file[fileno]
finally:
	epoll.unregister(serversocket.fileno())
	epoll.close()
	serversocket.close()
