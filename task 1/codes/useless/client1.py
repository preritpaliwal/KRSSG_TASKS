import socket
c = socket.socket()
print("trying to connect")
c.connect(("localhost",9998))
print("connected ig")
got = c.recv(1024).decode()
print("not got")
print(got)