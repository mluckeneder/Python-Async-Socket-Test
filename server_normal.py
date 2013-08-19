import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += b'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

file_name = "film.m4v"
try:
	while True:
		print("Serving a request")
		conn, address = serversocket.accept()
		request = b''
		while EOL1 not in request and EOL2 not in request:
			print("receiving...")
			request += conn.recv(1024)
		print('-'*40 + '\n' + request.decode()[:-2])
		# conn.send(response)

		with open(file_name, "rb") as f:
			while True:
				chunk = f.read(4096)
				if not chunk:
					break

				conn.send(chunk)
		conn.close()

finally:
	serversocket.close()

