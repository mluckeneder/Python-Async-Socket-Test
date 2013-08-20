# python -mtimeit -n1 -r2 'import client; client.test_client()'
# 1 loops, best of 2: 77.4 sec per loop
import socket
import os
import threading

class ClientThread(threading.Thread):
    """docstring for ClientThread"""
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def __run__(self):
        print("Running")




file_name = "../../Desktop/film.m4v"
file_size = os.path.getsize(file_name)
file_pointer = open(file_name, "rb")

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
response  = b'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += bytes("Content-Type: video/mp4\r\nContent-Length: %i\r\n\r\n" % (file_size), "ascii")


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))
serversocket.listen(1)

threads = []
try:

    while True:

        conn, address = serversocket.accept()
        thread = ClientThread(conn)
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

        # for fileno, event in events:
        #     if fileno == serversocket.fileno():
        #         conn, address = serversocket.accept()
        #         conn.setblocking(0)
        #         epoll.register(conn.fileno(), select.EPOLLIN)
        #         connections[conn.fileno()] = conn
        #         requests[conn.fileno()] = b''
        #         response_file[conn.fileno()] = 0
        #         responses[conn.fileno()] = 0

        #     elif event == select.EPOLLIN:
        #         requests[fileno] += connections[fileno].recv(1024)
        #         if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
        #             epoll.modify(fileno, select.EPOLLOUT)
        #             print('-'*40 + '\n' + requests[fileno].decode()[:-2])

        #     elif event == select.EPOLLOUT:
        #         header_p = responses[fileno]

        #         if header_p < len(response):
        #             byteswritten = connections[fileno].send(response[header_p:])
        #             responses[fileno] += byteswritten
        #         else:
        #             p = response_file[fileno]
        #             byteswritten = os.sendfile(fileno, file_pointer.fileno(), p, 8192)
        #             response_file[fileno] = p + byteswritten

        #         if response_file[fileno] == file_size:
        #             epoll.modify(fileno, 0)
        #             connections[fileno].shutdown(socket.SHUT_RDWR)


        #     elif event & select.EPOLLHUP:
        #         epoll.unregister(fileno)
        #         connections[fileno].close()
        #         del connections[fileno]
        #         del response_file[fileno]
finally:
    serversocket.close()
    file_pointer.close()
