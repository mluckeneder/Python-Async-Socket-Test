# Echo client program
import socket
import multiprocessing
import functools
import threading
import requests

def handle_client(tid):
    HOST = 'localhost'    # The remote host
    PORT = 8080              # The same port as used by the server
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((HOST, PORT))
    # s.send(b'GET /\n\r\n')
    with open("test%i.m4v" %(tid), "wb") as f:
        resp = requests.get('http://%s:%s' % (HOST, PORT))
        f.write(resp.content)

def test_client():
    print("Iteration")
    tasks = []
    for i in range(5):
        p = threading.Thread(target=functools.partial(handle_client, i))
        tasks.append(p)
        p.start()

    for t in tasks:
        t.join()

