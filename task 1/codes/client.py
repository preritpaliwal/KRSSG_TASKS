from threading import Thread
import socket
import pickle

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('localhost',3028))
s.listen()
c,adr = s.accept()
d = []
d = [float(item) for item in input("Enter the nos. to be added : ").split()]
c.send(pickle.dumps(d))
msg = pickle.loads(c.recv(1024))
print("sum = ",msg)
c.close()
