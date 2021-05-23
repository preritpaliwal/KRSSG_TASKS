import numpy as np 
import cv2
import math
from collections import deque

img  = cv2.imread("/home/tesla/Desktop/tasks/task 3/images/image 1.png",1)

node = np.full(img.shape,img.shape[0]+img.shape[1]+1,dtype = np.float32)
cv2.namedWindow("hello",cv2.WINDOW_NORMAL)
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.imshow("image",img)
cv2.waitKey(0)

black = [0, 0, 0]
grey = [127, 127, 127]
white = [255,255,255]
start = [113,204,45]
end = [60,76,231]
blue = [255,0,0]
red = [0,0,255]
green = [0,255,0]
magenta = [255,0,255]
dia = math.sqrt(2)
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
indexi = -1
indexj = -1

def bfs(x,y,find,color,scolor):
    node[x][y][0] = 0
    global indexi
    global indexj
    q = deque()
    q.append((x,y))
    i=0
    while(len(q)):
        i+=1
        if i%1 == 0:
            cv2.imshow("image",img)
            cv2.waitKey(1)
        i,j = q.popleft()
        img[i][j] = color
        if i+1<img.shape[0]:
            if comp(img[i+1][j],find):
                if(node[i+1][j][0]>node[i][j][0]+1):
                    node[i+1][j][0] = node[i][j][0]+1
                    node[i+1][j][1] = i
                    node[i+1][j][2] = j
                indexi = i+1
                indexj = j
                break
            # elif comp(img[i+1][j],black) or comp(img[i+1][j],red) or comp(img[i+1][j],grey):
            #     img[i+1][j] = scolor
            #     q.append((i+1,j))
            elif comp(img[i+1][j],white) or comp(img[i+1][j],color) or comp(img[i+1][j],scolor) or comp(img[i+1][j],start):
                pass
            else:
                if(node[i+1][j][0]>node[i][j][0]+1):
                    node[i+1][j][0] = node[i][j][0]+1
                    node[i+1][j][1] = i
                    node[i+1][j][2] = j
                img[i+1][j] = scolor
                q.append((i+1,j))
        if j+1<img.shape[1]:
            if comp(img[i][j+1],find):
                if(node[i][j+1][0]>node[i][j][0]+1):
                    node[i][j+1][0] = node[i][j][0]+1
                    node[i][j+1][1] = i
                    node[i][j+1][2] = j
                indexi = i
                indexj = j+1
                break
            # elif comp(img[i][j+1],black) or comp(img[i][j+1],red) or comp(img[i][j+1],grey):
            #     img[i][j+1] = scolor
            #     q.append((i,j+1))
            elif comp(img[i][j+1],white) or comp(img[i][j+1],color) or comp(img[i][j+1],scolor) or comp(img[i][j+1],start):
                pass
            else:
                if(node[i][j+1][0]>node[i][j][0]+1):
                    node[i][j+1][0] = node[i][j][0]+1
                    node[i][j+1][1] = i
                    node[i][j+1][2] = j
                img[i][j+1] = scolor
                q.append((i,j+1))
        if i-1>=0:
            if comp(img[i-1][j],find):
                if(node[i-1][j][0]>node[i][j][0]+1):
                    node[i-1][j][0] = node[i][j][0]+1
                    node[i-1][j][1] = i
                    node[i-1][j][2] = j
                indexi = i-1
                indexj = j
                break
            # elif comp(img[i-1][j],black) or comp(img[i-1][j],red) or comp(img[i-1][j],grey):
            #     img[i-1][j] = scolor
            #     q.append((i-1,j))
            elif comp(img[i-1][j],white) or comp(img[i-1][j],color) or comp(img[i-1][j],scolor) or comp(img[i-1][j],start):
                pass
            else:
                if(node[i-1][j][0]>node[i][j][0]+1):
                    node[i-1][j][0] = node[i][j][0]+1
                    node[i-1][j][1] = i
                    node[i-1][j][2] = j
                img[i-1][j] = scolor
                q.append((i-1,j))
        if j-1>=0:
            if comp(img[i][j-1],find):
                if(node[i][j-1][0]>node[i][j][0]+1):
                    node[i][j-1][0] = node[i][j][0]+1
                    node[i][j-1][1] = i
                    node[i][j-1][2] = j
                indexi = i
                indexj = j-1
                break
            # elif comp(img[i][j-1],black) or comp(img[i][j-1],red) or comp(img[i][j-1],grey):
            #     img[i][j-1] = scolor
            #     q.append((i,j-1))
            elif comp(img[i][j-1],white) or comp(img[i][j-1],color) or comp(img[i][j-1],scolor) or comp(img[i][j-1],start):
                pass
            else:
                if(node[i][j-1][0]>node[i][j][0]+1):
                    node[i][j-1][0] = node[i][j][0]+1
                    node[i][j-1][1] = i
                    node[i][j-1][2] = j
                img[i][j-1] = scolor
                q.append((i,j-1))
        if j-1>=0 and i-1>=0:
            if comp(img[i-1][j-1],find):
                if(node[i-1][j-1][0]>node[i][j][0]+dia):
                    node[i-1][j-1][0] = node[i][j][0]+dia
                    node[i-1][j-1][1] = i
                    node[i-1][j-1][2] = j
                indexi = i-1
                indexj = j-1
                break
            # elif comp(img[i][j-1],black) or comp(img[i][j-1],red) or comp(img[i][j-1],grey):
            #     img[i][j-1] = scolor
            #     q.append((i,j-1))
            elif comp(img[i-1][j-1],white) or comp(img[i-1][j-1],color) or comp(img[i-1][j-1],scolor) or comp(img[i-1][j-1],start):
                pass
            else:
                if(node[i-1][j-1][0]>node[i][j][0]+dia):
                    node[i-1][j-1][0] = node[i][j][0]+dia
                    node[i-1][j-1][1] = i
                    node[i-1][j-1][2] = j
                img[i-1][j-1] = scolor
                q.append((i-1,j-1))
        if j-1>=0 and i+1<img.shape[0]:
            if comp(img[i+1][j-1],find):
                if(node[i+1][j-1][0]>node[i][j][0]+dia):
                    node[i+1][j-1][0] = node[i][j][0]+dia
                    node[i+1][j-1][1] = i
                    node[i+1][j-1][2] = j
                indexi = i+1
                indexj = j-1
                break
            # elif comp(img[i][j-1],black) or comp(img[i][j-1],red) or comp(img[i][j-1],grey):
            #     img[i][j-1] = scolor
            #     q.append((i,j-1))
            elif comp(img[i+1][j-1],white) or comp(img[i+1][j-1],color) or comp(img[i+1][j-1],scolor) or comp(img[i+1][j-1],start):
                pass
            else:
                if(node[i+1][j-1][0]>node[i][j][0]+dia):
                    node[i+1][j-1][0] = node[i][j][0]+dia
                    node[i+1][j-1][1] = i
                    node[i+1][j-1][2] = j
                img[i+1][j-1] = scolor
                q.append((i+1,j-1))
        if j+1<img.shape[1] and i-1>=0:
            if comp(img[i-1][j+1],find):
                if(node[i-1][j+1][0]>node[i][j][0]+dia):
                    node[i-1][j+1][0] = node[i][j][0]+dia
                    node[i-1][j+1][1] = i
                    node[i-1][j+1][2] = j
                indexi = i-1
                indexj = j+1
                break
            # elif comp(img[i][j-1],black) or comp(img[i][j-1],red) or comp(img[i][j-1],grey):
            #     img[i][j-1] = scolor
            #     q.append((i,j-1))
            elif comp(img[i-1][j+1],white) or comp(img[i-1][j+1],color) or comp(img[i-1][j+1],scolor) or comp(img[i-1][j+1],start):
                pass
            else:
                if(node[i-1][j+1][0]>node[i][j][0]+dia):
                    node[i-1][j+1][0] = node[i][j][0]+dia
                    node[i-1][j+1][1] = i
                    node[i-1][j+1][2] = j
                img[i-1][j+1] = scolor
                q.append((i-1,j+1))
        if j+1<img.shape[1] and i+1<img.shape[0]:
            if comp(img[i+1][j+1],find):
                if(node[i+1][j+1][0]>node[i][j][0]+dia):
                    node[i+1][j+1][0] = node[i][j][0]+dia
                    node[i+1][j+1][1] = i
                    node[i+1][j+1][2] = j
                indexi = i+1
                indexj = j+1
                break
            # elif comp(img[i][j-1],black) or comp(img[i][j-1],red) or comp(img[i][j-1],grey):
            #     img[i][j-1] = scolor
            #     q.append((i,j-1))
            elif comp(img[i+1][j+1],white) or comp(img[i+1][j+1],color) or comp(img[i+1][j+1],scolor) or comp(img[i+1][j+1],start):
                pass
            else:
                if(node[i+1][j+1][0]>node[i][j][0]+dia):
                    node[i+1][j+1][0] = node[i][j][0]+dia
                    node[i+1][j+1][1] = i
                    node[i+1][j+1][2] = j
                img[i+1][j+1] = scolor
                q.append((i+1,j+1))
        
bfs(0,0,green,red,grey)
print(indexi,indexj)
bfs(indexi,indexj,red,blue,green)
print(indexi,indexj)
print(node[indexi][indexj])
a = indexi
b = indexj
for i in range(int(node[indexi][indexj][0])):
    img[int(a)][int(b)] = red
    c = node[int(a)][int(b)][1]
    b = node[int(a)][int(b)][2]
    a = c
    cv2.imshow("image",img)
    cv2.waitKey(5)

cv2.imshow("image",img)
node1 = np.full((img.shape[0],img.shape[1]),255,dtype = np.uint8)
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        node1[i][j] = int(node[i][j][0])
cv2.imshow("hello",node1)
cv2.waitKey(0)