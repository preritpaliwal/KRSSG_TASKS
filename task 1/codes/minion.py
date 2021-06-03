import socket
import pickle
from threading import Thread

def sum():
    arr = pickle.loads(c.recv(1024))
    print(arr,len(arr))

    sum = 0
    for i in range(len(arr)):
        sum+=arr[i]
    c.send(pickle.dumps(sum))
    print(sum)

c = socket.socket()
c.connect(('localhost',3031))
m = pickle.loads(c.recv(1024))
threads = []

for i in range(m):
    t = Thread(target=sum,args=[])
    threads.append(t)
    t.start()

for t in threads:
    t.join()