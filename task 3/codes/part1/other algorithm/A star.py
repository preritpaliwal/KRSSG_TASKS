import numpy as np 
import cv2
import math
from queue import PriorityQueue

img  = cv2.imread("/home/tesla/Desktop/tasks/task 3/codes/images/image 1.png",1)

node = np.full(img.shape,img.shape[0]+img.shape[1]+1,dtype = np.uint8)

cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.imshow("image",img)
cv2.waitKey(0)

black = [0, 0, 0]
grey = [127, 127, 127]
white = [255,255,255]
start = [27,216,17]
end = [13,13,243]
blue = [255,0,0]
red = [0,0,255]
yellow = [0,255,255]
green = [0,255,0]
magenta = [255,0,255]
 
img = cv2.resize(img,(120,120), interpolation = cv2.INTER_AREA)


def thresh_white(a):
    k=0
    for i in range(3):
        if a[i]>200:
            k+=1
    if k==3:
        return white
    else:
        return a

def thresh_green(a):
    k=0
    if a[0]<100:
        k+=1
    if a[1]>200:
        k+=1
    if a[2]<100:
        k+=1
    if k==3:
        return green
    else:
        return a

def thresh_red(a):
    k=0
    if a[0]<100:
        k+=1
    if a[2]>200:
        k+=1
    if a[1]<100:
        k+=1
    if k==3:
        return red
    else:
        return a
def thresh(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = thresh_white(img[i][j])
            img[i][j] = thresh_green(img[i][j])
            img[i][j] = thresh_red(img[i][j])

# heuristic - eucledian distance
def comp(a1,a2):
    k = 0 
    # print(a1)
    # print(a2)
    for i in range(3):
        if a1[i] == a2[i]:
            k+=1
    if k == 3:
        return 1
    else:
        return 0

def f(i,j):
    global ie,je
    return math.sqrt((i-ie)**2 + (j-je)**2) + node[i][j][0]

def A(ib,jb):
    global ie,je
    q = PriorityQueue()
    node[ib][jb][0] = 0
    q.put((f(ib,jb),(ib,jb)))
    t = 0
    while(q.qsize()):
        t+=1
        cost,(i,j) = q.get()
        img[i][j] = blue
        if t%10 == 0:
            cv2.imshow("image",img)
            cv2.waitKey(1)
        if i-1>=0:
            if i-1 == ie and j ==je:
                if node[i-1][j][0] > node[i][j][0] + 1:
                    node[i-1][j][0] = node[i][j][0] + 1
                    node[i-1][j][1] = i
                    node[i-1][j][2] = j
                    print("in1")
                print("out1")
                print(i-1,j)
                break
            elif comp(img[i-1][j],blue) or comp(img[i-1][j],green) or comp(img[i-1][j],white):
                pass
            else:
                img[i-1][j] = green
                if node[i-1][j][0] > node[i][j][0]+1:
                    node[i-1][j][0] = node[i][j][0] + 1
                    node[i-1][j][1] = i
                    node[i-1][j][2] = j
                q.put((f(i-1,j),(i-1,j)))
        if j-1>=0:
            if i == ie and j-1 ==je:
                if node[i][j-1][0] > node[i][j][0] + 1:
                    node[i][j-1][0] = node[i][j][0] + 1
                    node[i][j-1][1] = i
                    node[i][j-1][2] = j
                    print("in2")
                print("out2")
                print(i,j-1)
                break
            elif comp(img[i][j-1],blue) or comp(img[i][j-1],green) or comp(img[i][j-1],white):
                pass
            else:
                img[i][j-1] = green
                if node[i][j-1][0] > node[i][j][0]+1:
                    node[i][j-1][0] = node[i][j][0] + 1
                    node[i][j-1][1] = i
                    node[i][j-1][2] = j
                q.put((f(i,j-1),(i,j-1)))
        if i+1<img.shape[0]:
            if i+1 == ie and j ==je:
                if node[i+1][j][0] > node[i][j][0] + 1:
                    node[i+1][j][0] = node[i][j][0] + 1
                    node[i+1][j][1] = i
                    node[i+1][j][2] = j
                    print("in3")
                print("out3")
                print(i+1,j)
                break
            elif comp(img[i+1][j],blue) or comp(img[i+1][j],green) or comp(img[i+1][j],white):
                pass
            else:
                img[i+1][j] = green
                if node[i+1][j][0] > node[i][j][0]+1:
                    node[i+1][j][0] = node[i][j][0] + 1
                    node[i+1][j][1] = i
                    node[i+1][j][2] = j
                q.put((f(i+1,j),(i+1,j)))
        if j+1<img.shape[1]:
            if i == ie and j+1 ==je:
                if node[i][j+1][0] > node[i][j][0] + 1:
                    node[i][j+1][0] = node[i][j][0] + 1
                    node[i][j+1][1] = i
                    node[i][j+1][2] = j
                    print("in4")
                print("out4")
                print(i,j+1)
                break
            elif comp(img[i][j+1],blue) or comp(img[i][j+1],green) or comp(img[i][j+1],white):
                pass
            else:
                img[i][j+1] = green
                if node[i][j+1][0] > node[i][j][0]+1:
                    node[i][j+1][0] = node[i][j][0] + 1
                    node[i][j+1][1] = i
                    node[i][j+1][2] = j
                q.put((f(i,j+1),(i,j+1)))
        

ib,jb = 10,10
ie = 110
je = 110

thresh(img)

A(ib,jb)
a = ie
b = je

print(a,b,ie,je)
for i in range(node[ie][je][0]):
    print(a,b)
    img[a][b] = red
    c = node[a][b][1]
    b = node[a][b][2]
    a = c
    cv2.imshow("image",img)
    cv2.waitKey(5)

print(node[ie][je])
cv2.imshow("image",img)
cv2.waitKey(0)