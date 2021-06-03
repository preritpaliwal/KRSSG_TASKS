import socket
import pickle

c = socket.socket()
c.connect(('localhost',1235))
data = c.recv(4096)
# Decode received data into UTF-8
data = pickle.loads(data)
# Convert decoded data into list
# data = eval(data)
print(data,len(data))