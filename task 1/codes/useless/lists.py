import socket
import pickle

s = socket.socket()
s.bind(('localhost',1235))
s.listen()
y=[0,12,6,8,3,2,10] 
data=pickle.dumps(y)
print(y,data)
c,adr = s.accept()

c.send(data)
c.close()