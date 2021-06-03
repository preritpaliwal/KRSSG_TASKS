from threading import Thread
import socket

class sendingthread(Thread):
    def __init__(self,mysocket):
        Thread.__init__(self)
        self.c  =mysocket

    def run(self):
        while True:
            data = input()
            # print("printing from thread ",data)
            self.c.send(bytes(data,'utf-8'))

class receivingthread(Thread):
    def __init__(self,mysocket):
        Thread.__init__(self)
        self.c =mysocket

    def run(self):
        while True:
            msg = self.c.recv(1024).decode('utf-8')
            print('printing after receiving from 1 ',msg)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('localhost',2010))
# s.listen()
# c,adr = s.accept()
st = sendingthread(s)
rt = receivingthread(s)
st.start()
rt.start()
