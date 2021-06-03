import socket
c = socket.socket()
c.connect(('localhost',3031))
arr = c.recv(1024).decode('utf-8')
print(arr,len(arr))
a = []

start = 0
end = -1
for i in range(len(arr)):
    if arr[i]==',':
        start = end +1
        end = i
        num = 0
        minus = False
        # print(start,end)
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
n = 0
# print(end,start,len(arr))
minus = False
for i in range(end+2,len(arr)-1,1):
    
    if arr[i] == '-':
        minus = True
        continue
    n = 10*n + int(arr[i])
if minus:
    a.append(-n)
else:
    a.append(n)
print(a,len(a))
sum = 0
for i in range(len(a)):
    sum+=a[i]
c.send(bytes(str(sum),'utf-8'))
print(sum)