from threading import Thread
import socket

s = socket.socket()
s.bind(('localhost',3031))
s.listen()
c = socket.socket()
c.connect(('localhost',3027))
arr = c.recv(1024).decode('utf-8')
print(arr,len(arr))
a = []
# for i in range(int((len(arr)+1)/2)):
#     a.append(int(arr[2*i]))
start = -1
end = -1
for i in range(len(arr)):
    if arr[i]==' ':
        start = end
        end = i
        num = 0
        minus = False
        for j in range(start+1,end,1):
            if arr[j]=='-':
                minus = True
                continue
            num = 10*num + int(arr[j])
        if minus:
            a.append(-num)
            # print(a[-1])
        else:
            a.append(num)
            # print(a[-1])
        minus = False

n = 0
min = False
for i in range(end+1,len(arr),1):
    if arr[i]=='-':
        min= True
        continue
    n = 10*n + int(arr[i])
if min:
    a.append(-n)
else:
    a.append(n)
print(a)
m = int(input())
msum = []
threads = []

def fx(k):
    global m
    array = []
    n = len(a)
    print(int(k*n/m),n)
    for i in range(int((k-1)*n/m),int(k*n/m),1):
        array.append(a[i])
    c,adr = s.accept()
    print("connect to ",adr, array)
    c.send(bytes(str(array),'utf-8'))
    msg = c.recv(1024).decode('utf-8')
    msum.append(int(msg))
    print(f"thread {k} got this {int(msg)}")


for i in range(0,m,1):
    t = Thread(target=fx,args=[i+1])
    t.start()
    threads.append(t)

for t in threads:
    t.join()

sum = 0
for i in range(m):
    sum+=msum[i]

c.send(bytes(str(sum),'utf-8'))
print("sum send : ",sum)