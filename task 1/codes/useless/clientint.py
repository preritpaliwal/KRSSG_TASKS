from threading import Thread
import socket

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(('localhost',3027))
s.listen()
c,adr = s.accept()
data = input()
c.send(bytes(data,'utf-8'))
msg = c.recv(1024).decode('utf-8')
print(msg)
c.close()
