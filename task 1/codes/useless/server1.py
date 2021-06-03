import socket
s = socket.socket()
s.bind(('localhost',9998))
s.listen(3)
print("listeneing")
while True:
    c,adr = s.accept()
    print("address is ",adr)
    # while True:
    #     pass
    # c.send(bytes("hi client",'utf-8'))
    # c.close() 