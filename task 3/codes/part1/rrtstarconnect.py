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
brown = [19,69,139]
orange = [0,140,255]

class RRTMap:
    def __init__(self,img):
        self.img = img

    def drawPath(self,path):
        x,y = -1,-1
        for i in path:
            if x != -1:
                cv2.line(self.img,(x,y),(i[0],i[1]),orange,2)
            x,y = i
            cv2.circle(self.img, (x,y),4,yellow,-1)


    def erasePath(self,path):
        x,y = -1,-1
        for i in path:
            if x != -1:
                cv2.line(self.img,(x,y),(i[0],i[1]),black,2)
                cv2.line(self.img,(x,y),(i[0],i[1]),blue,1)
            x,y = i
            cv2.circle(self.img, (x,y),4,black,-1)
            cv2.circle(self.img, (x,y),2,magenta,-1)
        
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
        self.cost = []
        #initializing the tree
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        self.cost.append(0)
        #path
        self.goalstate = None
        self.path = []
        #image
        self.img = img

    def add_node(self,x,y):
        self.x.append(x)
        self.y.append(y)

    def show_node(self,x,y):
        cv2.circle(self.img,(x,y),2,magenta,-1)
        
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

# to find node nearest to nth node
    def nearest(self,n):                                                      
        dmin = self.distance(0,n)
        nnear = 0
        for i in range(n):
            d = self.distance(i,n)
            if d<dmin:
                dmin = d
                nnear = i
        return nnear
                
# to check if node is not on the obstacle
    def isFree(self):
        n = self.number_of_nodes()-1
        (x,y) = (self.x[n],self.y[n])
        if y>=self.img.shape[0] or y<0 or x>=self.img.shape[1] or x<0:
            self.remove_node(n)
            return False
        if comp(self.img[y][x],white) or comp(self.img[y][x],magenta):
            self.remove_node(n)
            return False
        else:
            return True

# to check if line joining nodes crosses obsctacle 
    def crossObstacle(self,x1,y1,x2,y2):
        for i in range(0,101):
            u = i/100
            x = int(x1*u + x2*(1-u))
            y = int(y1*u + y2*(1-u))
            if comp(self.img[y][x],white):
                return True
        return False

# to connect nodes
    def connect(self,n1,n2):
        x1,y1,x2,y2 = self.x[n1],self.y[n1],self.x[n2],self.y[n2]
        if self.crossObstacle(x1,y1,x2,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True

# adds a random node at a max distance of dmax
    def step(self,nnear,nrand):
        global dmax
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
        self.add_node(x,y)
        # if ((self.x[nnear]-self.goal[0])**2 + (self.y[nnear]- self.goal[1])**2)**0.5 < dmax:
        #     self.add_node(self.goal[0],self.goal[1])
        # else:

        if self.isFree():
            return True
        else:
            return False

# generates the path to goal
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

# expands the tree in random direction
    def expand(self,x,y):
        global radius
        n = self.number_of_nodes()
        # x,y = self.random_choice()
        self.add_node(x,y)
        f = 0
        nnearest = self.nearest(n)
        if self.step(nnearest,n):
            if self.connect(nnearest,n):
                cmin = self.cost[nnearest] + self.distance(nnearest,n)
                nnear = nnearest
                local = []
                for i in range(n):
                    if self.distance(i,n)<radius:
                        local.append(i)
                        if cmin>(self.cost[i] + self.distance(i,n)):
                            cmin = self.cost[i] + self.distance(i,n)
                            nnear = i
                self.remove_edge(n)
                if self.connect(nnear,n):
                    self.cost.append(cmin)
                    f = 1
                    for i in local:
                        if not self.crossObstacle(self.x[i],self.y[i],self.x[n],self.y[n]):
                            if self.cost[i] > (self.cost[n] + self.distance(i,n)):
                                cv2.line(self.img,(self.x[i],self.y[i]),(self.x[self.parent[i]],self.y[self.parent[i]]),black,1)
                                self.remove_edge(i)
                                self.add_edge(n,i)
                                cv2.line(self.img,(self.x[i],self.y[i]),(self.x[n],self.y[n]),blue,1)
                                self.cost[i] = self.cost[n] + self.distance(i,n)

        return self.x,self.y,self.parent,f

# expands the tree towards goal
    def bias(self,goal):
        global radius
        n = self.number_of_nodes()
        self.add_node(goal[0],goal[1])
        nnearest = self.nearest(n)
        f=0
        if self.step(nnearest,n):
            if self.connect(nnearest,n):
                cmin = self.cost[nnearest] + self.distance(nnearest,n)
                nmin = nnearest
                local = []
                for i in range(n):
                    if self.distance(i,n)<radius:
                        local.append(i)
                        if cmin>(self.cost[i] + self.distance(i,n)):
                            cmin = self.cost[i] + self.distance(i,n)
                            nmin = i
                self.remove_edge(n)
                if self.connect(nmin,n):
                    self.cost.append(cmin)
                    f=1
                    if comp(self.img[self.y[-1]][self.x[-1]],red):
                        self.add_node(self.goal[0],self.goal[1])
                        self.cost.append(self.cost[-1] + self.distance(n,n+1))
                        self.add_edge(n,n+1)
                        self.show_node(self.goal[0],self.goal[1])
                        cv2.line(self.img,(self.x[-2],self.y[-2]),(self.x[-1],self.y[-1]),blue,1)
                        self.goalstate = n+1
                        self.flag = True
                    for i in local:
                        if not self.crossObstacle(self.x[i],self.y[i],self.x[n],self.y[n]):
                            if self.cost[i] > (self.cost[n] + self.distance(i,n)):
                                cv2.line(self.img,(self.x[i],self.y[i]),(self.x[self.parent[i]],self.y[self.parent[i]]),black,1)
                                self.remove_edge(i)
                                self.add_edge(n,i)
                                cv2.line(self.img,(self.x[i],self.y[i]),(self.x[n],self.y[n]),blue,1)
                                self.cost[i] = self.cost[n] + self.distance(i,n)

        return self.x,self.y,self.parent,f

    def update_goal(self,g):
        self.goal = g

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


# dmax for a step and Radius for rewiring of tree
dmax  = 200
radius = 20


def main():
    path1  = "/home/tesla/Desktop/tasks/task 3/images/image 1.png"
    # pathark = "/home/tesla/Desktop/image.jpg"
    path2 = "/home/tesla/Desktop/tasks/task 3/images/image 2.png"
    start1 = (30,28)
    start2 = (97,29)
    start3 = (29,257)
    goal2 = (204,312)
    goal1 = (367,107)
    goal3 = (359,307)

    img = cv2.imread(path2,1)
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    show(img,0)

    thresh(img)

# finding center of start and goal in image 1
    # start = start_f(img)
    # goal = end_f(img)

    map = RRTMap(img)
    graph1 = RRTGraph(start1,goal3,(img.shape[0],img.shape[1]),img)
    graph2 = RRTGraph(goal3,start1,(img.shape[0],img.shape[1]),img)
    iterations = 0
    k=0
    graph1.show_node(start1[0],start1[1])

    t1 = time.time()
    time_to_run = 60
    p4 = []
    
    while iterations<3000:

        elapsed = time.time() - t1
        if elapsed > time_to_run:
            break
        
        xrand,yrand = graph1.random_choice()
        x1,y1,parent1,f1 = graph1.expand(xrand,yrand)
        if f1 == 1:
            graph1.show_node(x1[-1],y1[-1])
            cv2.line(img,(x1[-1],y1[-1]),(x1[parent1[-1]],y1[parent1[-1]]),blue,1)
            cmin2 = img.shape[0]  + img.shape[1]
            inear2 = -1
            for i in range(graph2.number_of_nodes()):
                if (((graph2.x[i]-x1[-1])**2 + (graph2.y[i]-y1[-1])**2)**0.5) <radius:
                    if not graph1.crossObstacle(graph2.x[i],graph2.y[i],x1[-1],y1[-1]):
                        if cmin2 > graph2.cost[i]:
                            cmin2 = graph2.cost[i]
                            inear2 = i

            if inear2 != -1:
                x1,y1,parent1,f1 = graph1.expand(graph2.x[inear2],graph2.y[inear2])
                if f1 == 1:    
                    graph2.expand(x1[parent1[-1]],y1[parent1[-1]])
                    cv2.line(img,(x1[-1],y1[-1]),(x1[parent1[-1]],y1[parent1[-1]]),blue,1)
                    if graph1.goalstate == None:
                        graph1.goalstate = graph1.number_of_nodes()-1
                        graph1.flag = True
                        graph2.goalstate = inear2
                        graph2.flag = True
                    elif (graph1.cost[graph1.goalstate] + graph2.cost[graph2.goalstate]) > (graph1.cost[-1] + graph2.cost[inear2]):
                        graph1.goalstate = graph1.number_of_nodes()-1
                        graph2.goalstate = inear2

        xrand,yrand = graph2.random_choice()
        x2,y2,parent2,f2 = graph2.expand(xrand,yrand)
        if f2 == 1:
            graph2.show_node(x2[-1],y2[-1])
            cv2.line(img,(x2[-1],y2[-1]),(x2[parent2[-1]],y2[parent2[-1]]),blue,1)
            cmin1 = img.shape[0]  + img.shape[1]
            inear1 = -1
            for i in range(graph1.number_of_nodes()):
                if (((graph1.x[i]-x2[-1])**2 + (graph1.y[i]-y2[-1])**2)**0.5) <radius:
                    if not graph1.crossObstacle(graph1.x[i],graph1.y[i],x2[-1],y2[-1]):
                        if cmin1 > graph1.cost[i]:
                            cmin1 = graph1.cost[i]
                            inear1 = i

            if inear1 != -1:
                x2,y2,parent2,f2 = graph2.expand(graph1.x[inear1],graph1.y[inear1])
                if f2 == 1:    
                    graph1.expand(x2[parent2[-1]],y2[parent2[-1]])
                    cv2.line(img,(x2[-1],y2[-1]),(x2[parent2[-1]],y2[parent2[-1]]),blue,1)
                    if graph2.goalstate == None:
                        graph2.goalstate = graph2.number_of_nodes()-1
                        graph1.flag = True
                        graph1.goalstate = inear1
                        graph2.flag = True
                    elif (graph1.cost[graph1.goalstate] + graph2.cost[graph2.goalstate]) > (graph2.cost[-1] + graph1.cost[inear1]):
                        graph2.goalstate = graph2.number_of_nodes()-1
                        graph1.goalstate = inear1

        iterations+=1
        print(f"iteration  = {iterations}")
        if graph1.path_to_goal() and graph2.path_to_goal():
            p1 = graph1.getPathCoords()
            p2 = graph2.getPathCoords()
            p1.reverse()
            p3 = p1 + p2
            if len(p4) == 0:
                map.drawPath(p3)
                p4 = p3
            elif p3 != p4 :
                map.erasePath(p4)
                p4 = p3
                map.drawPath(p4)
                cv2.waitKey(1)
        show(img,1)
    show(img)
    
    return 0

if __name__=='__main__':
    main()