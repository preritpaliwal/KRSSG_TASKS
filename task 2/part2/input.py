import socket
import pickle
import sys, select

c = socket.socket()
c.connect(('localhost',3036))

while True:
    i, o, e = select.select( [sys.stdin], [], [], 1 )
    if i:
        s = sys.stdin.readline().strip()
    else:
        s = 'q'
    
    c.send(pickle.dumps(s))
