from threading import Thread
import pickle
import socket

s = socket.socket()
s.bind(('localhost',3031))
s.listen()
c1 = socket.socket()
c1.connect(('localhost',3028))
arr = pickle.loads(c1.recv(1024))
print(arr,len(arr))
c,adr = s.accept()

m = int(input("enter no.of minions : "))
c.send(pickle.dumps(m))
msum = []
threads = []

def fx(k):
    global m
    array = []
    n = len(arr)
    # print(int(k*n/m),n)
    for i in range(int((k-1)*n/m),int(k*n/m),1):
        array.append(arr[i])
    print("connect to ",adr, array)
    c.send(pickle.dumps(array))
    msg = pickle.loads(c.recv(1024))
    msum.append(msg)
    print(f"thread {k} got this {msg}")


for i in range(0,m,1):
    t = Thread(target=fx,args=[i+1])
    t.start()
    threads.append(t)

for t in threads:
    t.join()

sum = 0
for i in range(m):
    sum+=msum[i]

c1.send(pickle.dumps(sum))
print("sum send : ",sum)