import math
import random
import math
import cv2
import numpy as np
import time

# colors
black = [0, 0, 0]
grey = [127, 127, 127]
white = [255,255,255]
blue = [255,0,0]
red = [0,0,255]
green = [0,255,0]
magenta = [255,0,255]
yellow = [0,255,255]

class RRTMap:
    def __init__(self,start,goal,mapdim,img):
        self.start = start
        self.goal = goal
        self.h,self.w = mapdim
        self.img = img

    def drawMap(self):
        pass

    def drawPath(self,path):
        for i in path:
            x,y = i
            self.img[y][x] = yellow
            if y+1<self.img.shape[0]:
                self.img[y+1][x] = yellow
            if y-1>-1:
                self.img[y-1][x] = yellow
            if x-1>-1:
                self.img[y][x-1] = yellow
            if x+1<self.img.shape[1]:
                self.img[y][x+1] = yellow
            if y-2>-1:
                self.img[y-2][x] = yellow
            if y+2<self.img.shape[0]:
                self.img[y+2][x] = yellow
            if y-1>-1 and x-1>-1:
                self.img[y-1][x-1] = yellow
            if y+1<self.img.shape[0] and x-1>-1:
                self.img[y+1][x-1] = yellow
            if y-1>-1 and x+1<self.img.shape[1]:
                self.img[y-1][x+1] = yellow
            if y+1<self.img.shape[0] and x+1<self.img.shape[1]:
                self.img[y+1][x+1] = yellow
            if x-2>-1:
                self.img[y][x-2] = yellow
            if x+2<self.img.shape[1]:
                self.img[y][x+2] = yellow
        
    def erasePath(self,path):
        for i in path:
            x,y = i
            cv2.circle(self.img, (x,y),2,black,-1)
            cv2.circle(self.img, (x,y),1,magenta,-1)


class RRTGraph:
    def __init__(self,start,goal,mapdim,img):
        (x,y) = start
        self.start = start
        self.goal = goal
        self.flag = False
        self.h,self.w = mapdim
        self.x=[]
        self.y=[]  
        self.parent=[]
        #initializing the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        #path
        self.goalstate = None
        self.path = []
        #image
        self.img = img

    def updateGoal(self,g):
        self.goal = g

    def add_node(self,x,y):
        self.x.append(x)
        self.y.append(y)

    def show_node(self,x,y):
        self.img[y][x] = magenta
        if y+1<self.img.shape[0]:
            self.img[y+1][x] = magenta
        if y-1>-1:
            self.img[y-1][x] = magenta
        if x-1>-1:
            self.img[y][x-1] = magenta
        if x+1<self.img.shape[1]:
            self.img[y][x+1] = magenta
        

    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self,parent,child):
        self.parent.insert(child,parent)

    def remove_edge(self,n):
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self,n1,n2):
        return math.sqrt((self.x[n1]-self.x[n2])**2 + (self.y[n1]-self.y[n2])**2)

    def random_choice(self):
        x = random.randint(0,self.w-1)
        y = random.randint(0,self.h-1)
        return x,y

    def nearest(self,n):
        dmin = self.distance(0,n)
        nnear = 0
        for i in range(n):
            d = self.distance(i,n)
            if d<dmin:
                dmin = d
                nnear = i
        return nnear
                

    def isFree(self):
        n = self.number_of_nodes()-1
        (x,y) = (self.x[n],self.y[n])
        if y>self.img.shape[0] or y<0 or x>self.img.shape[1] or x<0:
            self.remove_node(n)
            return False
        if comp(self.img[y][x],white):
            self.remove_node(n)
            return False
        else:
            return True

    def crossObstacle(self,x1,y1,x2,y2):
        for i in range(0,101):
            u = i/100
            x = int(x1*u + x2*(1-u))
            y = int(y1*u + y2*(1-u))
            if comp(self.img[y][x],white):
                return True
        return False

    def connect(self,n1,n2):
        x1,y1,x2,y2 = self.x[n1],self.y[n1],self.x[n2],self.y[n2]
        if self.crossObstacle(x1,y1,x2,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            if x2==self.goal[0] and y2 == self.goal[1]:
                self.goalstate = n2
                self.flag = True
            return True

    def step(self,nnear,nrand,dmax = 100):
        d = self.distance(nnear,nrand)
        if d>dmax:
            u = dmax/d
            (xnear,ynear) = (self.x[nnear],self.y[nnear])
            (xrand,yrand) = (self.x[nrand],self.y[nrand])
            theta = math.atan2((yrand-ynear),(xrand-xnear))
            (x,y) =  (int(xnear + dmax*math.cos(theta)),int(ynear + dmax*math.cos(theta)))
            
        else:
            (x,y) = (self.x[nrand],self.y[nrand])
        
        self.remove_node(nrand)
        if abs(x-self.goal[0])<dmax and abs(y - self.goal[1])<dmax:
            self.add_node(self.goal[0],self.goal[1])
        else:
            self.add_node(x,y)

        if self.isFree():
            return True
        else:
            return False

    def path_to_goal(self):
        if self.flag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while(newpos!=0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)
        return self.flag

    def getPathCoords(self):
        pathcoords = []
        for i in self.path:
            pathcoords.append((self.x[i],self.y[i]))
        return pathcoords

    def bias(self,goal):
        n = self.number_of_nodes()
        self.add_node(goal[0],goal[1])
        f = 0
        nnear = self.nearest(n)
        if self.step(nnear,n):
            if self.connect(nnear,n):
                f = 1
        return self.x,self.y,self.parent,f

    def expand(self,x,y):
        n = self.number_of_nodes()
        f= 0
        # x,y = self.random_choice()
        self.add_node(x,y)
        nnearest = self.nearest(n)
        if self.step(nnearest,n):
            if self.connect(nnearest,n):
                f =1
        return self.x,self.y,self.parent,f

    def cost(self):
        pass

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

def comp(a1,a2):
    k = 0 
    for i in range(3):
        if a1[i] == a2[i]:
            k+=1
    if k == 3:
        return True
    else:
        return False

def start_f(img):
    k = 0
    sumi = 0
    sumj = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if comp(img[i][j],green):
                sumi+=i
                sumj+=j
                k+=1
    return (int(sumj/k),int(sumi/k))

def end_f(img):
    k = 0
    sumi = 0
    sumj = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if comp(img[i][j],red):
                sumi+=i
                sumj+=j
                k+=1
    return (int(sumj/k),int(sumi/k))

def show(img,a= 0):
    cv2.imshow("image",img)
    cv2.waitKey(a)

def main():
    path1  = "/home/tesla/Desktop/tasks/task 3/images/image 1.png"
    # pathark = "/home/tesla/Desktop/image.jpg"
    path2 = "/home/tesla/Desktop/tasks/task 3/images/image 2.png"
    img = cv2.imread(path1,1)
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    show(img,0)

    thresh(img)
    start = start_f(img)
    goal = end_f(img)

    map = RRTMap(start,goal,(img.shape[0],img.shape[1]),img)
    graph1 = RRTGraph(start,goal,(img.shape[0],img.shape[1]),img)
    graph2 = RRTGraph(goal,start,(img.shape[0],img.shape[1]),img)
    iterations = 0
    graph1.show_node(start[0],start[1])
    show(img)

    while not (graph1.path_to_goal() and graph2.path_to_goal()):

        # if iterations%10==10:
        #     x,y,parent = graph.bias(goal)
        #     graph.show_node(x[-1],y[-1])
        #     cv2.line(img,(x[-1],y[-1]),(x[parent[-1]],y[parent[-1]]),blue,1)
        # else:
        xrand,yrand = graph1.random_choice()
        x1,y1,parent1,f1 = graph1.expand(xrand,yrand)
        # print(f"f1 = {f1}")
        if f1 == 1:
            # print("node added")
            graph1.show_node(x1[-1],y1[-1])
            cv2.line(img,(x1[-1],y1[-1]),(x1[parent1[-1]],y1[parent1[-1]]),blue,1)
            graph2.updateGoal((x1[-1],y1[-1]))
            last_node2 = [-1,-1]
            while 1:
                x2,y2,parent2,f2 = graph2.bias((x1[-1],y1[-1]))
                if f2 == 0:
                    break
                graph2.show_node(x2[-1],y2[-1])
                cv2.line(img,(x2[-1],y2[-1]),(x2[parent2[-1]],y2[parent2[-1]]),blue,1)
                if last_node2 == [x2[-1],y2[-1]]:
                    break
                last_node2 = [x2[-1],y2[-1]]

        xrand,yrand = graph2.random_choice()
        x2,y2,parent2,f2 = graph2.expand(xrand,yrand)
        if f2 == 1:
            graph2.show_node(x2[-1],y2[-1])
            cv2.line(img,(x2[-1],y2[-1]),(x2[parent2[-1]],y2[parent2[-1]]),blue,1)
            graph1.updateGoal((x2[-1],y2[-1]))
            last_node1 = [-1,-1]
            while 1:
                x1,y1,parent1,f1 = graph1.bias((x2[-1],y2[-1]))
                if f1 == 0:
                    break
                graph2.show_node(x1[-1],y1[-1])
                cv2.line(img,(x1[-1],y1[-1]),(x1[parent1[-1]],y1[parent1[-1]]),blue,1)
                if last_node1 == [x1[-1],y1[-1]]:
                    break
                last_node1 = [x1[-1],y1[-1]]
        iterations+=1
        print(f"iteration  = {iterations}")
        show(img,1)
    map.drawPath(graph1.getPathCoords())
    map.drawPath(graph2.getPathCoords())
    show(img)
    return 0

if __name__=='__main__':
    main()