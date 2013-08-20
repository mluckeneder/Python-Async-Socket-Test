# Echo client program
import socket
import multiprocessing
import threading

def handle_client(tid):
	HOST = '192.168.169.143'    # The remote host
	PORT = 8080              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.send(b'GET /\n\r\n')
	with open("test%i.m4v" %(tid), "wb") as f:
		while True:
			data = s.recv(8192)
			# print("recv")
			if not data:
				break

			f.write(data)



	s.close()
def test_client():
	print("Iteration")
	tasks = []
	for i in range(5):
		p = threading.Thread(target=handle_client, args=(i,))
		tasks.append(p)
		p.start()

	for t in tasks:
		t.join()

