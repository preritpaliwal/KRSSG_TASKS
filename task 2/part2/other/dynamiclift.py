from threading import Thread
from time import sleep, time
import numpy as np
import socket
import pickle

from numpy.lib.function_base import append

s = socket.socket()
s.bind(('localhost',3035))
s.listen()
c,adr = s.accept()
# states
class rest():
    def __init__(self):
        self.state = "rest"
    def execute(self):
        pass

class up():
    def __init__(self):
        self.state = "up"
    def execute(self):
        pass

class down():
    def __init__(self):
        self.state = "down"
    def execute(self):
        pass

# =================================================================================

class transistion():
    def __init__(self,tostate):
        self.tostate = tostate

    def execute(self):
        pass

class finitestatemachine():
    def __init__(self):
        self.states = {}
        self.transitions = {}
        self.curstate = None
        self.trans = None

    def setstate(self,statename):
        self.curstate = self.states[statename]

    def transition(self,transname):
        self.trans = self.transitions[transname]

    def execute(self):
        if(self.trans):
            self.trans.execute()
            self.setstate(self.trans.tostate)
            self.trans = None
        self.curstate.execute()

class lift():
    def __init__(self):
        self.currentfloor = 0
        self.direction = 0
        self.fsm = finitestatemachine()
        self.distance = 0

    def move(self):
        print(f"from {self.currentfloor}",end=" ")
        if(self.fsm.curstate.state=="up"):
            self.currentfloor+=1
            self.distance+=1
            self.direction = 1
        if(self.fsm.curstate.state=="down"):
            self.currentfloor+=(-1)
            self.distance+=1
            self.direction = -1
        if(self.fsm.curstate.state=="rest"):
            self.currentfloor+=(0)
        print("to ",self.currentfloor)
        msg =  pickle.loads(c.recv(1024))
        # print(msg)
        if msg == "q":
            pass
        else:
            getpassengers(msg)


class system():
    def __init__(self):
        self.l1 = lift()
        self.l2 = lift()


class passenger():
    def __init__(self,start,dir,end):
        self.start = start
        self.dir = dir
        self.end = end


def distributep():
    p,n = passengers[-1],len(passengers)
    # if n%2==1:
    #     passengers1.append(n-1)
    # else:
    #     passengers2.append(n-1)
    if syst.l1.currentfloor>=syst.l2.currentfloor:
        if syst.l1.direction==-1 and syst.l2.direction==1:
            if p.start>=syst.l1.currentfloor:
                passengers2.append(n-1)
            elif p.start<syst.l1.currentfloor and p.start>syst.l2.currentfloor:
                if p.dir=='u':
                    passengers2.append(n-1)
                else:
                    passengers1.append(n-1)
            else:
                passengers1.append(n-1)
        if syst.l1.direction==1 and syst.l2.direction==-1:
            if p.start>=syst.l1.currentfloor:
                passengers1.append(n-1)
            elif p.start<syst.l1.currentfloor and p.start>syst.l2.currentfloor:
                if p.dir=='u':
                    passengers2.append(n-1)
                else:
                    passengers1.append(n-1)
            else:
                passengers2.append(n-1)
        if syst.l1.direction==1 and syst.l2.direction==1:
            if p.start>=syst.l1.currentfloor:
                passengers1.append(n-1)
            elif p.start<syst.l1.currentfloor and p.start>syst.l2.currentfloor:
                if p.dir=='u':
                    passengers2.append(n-1)
                else:
                    passengers1.append(n-1)
            else:
                passengers1.append(n-1)
        if syst.l1.direction==-1 and syst.l2.direction==-1:
            if p.start>=syst.l1.currentfloor:
                passengers2.append(n-1)
            elif p.start<syst.l1.currentfloor and p.start>syst.l2.currentfloor:
                if p.dir=='u':
                    passengers2.append(n-1)
                else:
                    passengers1.append(n-1)
            else:
                passengers2.append(n-1)
    else:
        if syst.l2.direction==-1 and syst.l1.direction==1:
            if p.start>=syst.l2.currentfloor:
                passengers1.append(n-1)
            elif p.start<syst.l2.currentfloor and p.start>syst.l1.currentfloor:
                if p.dir=='u':
                    passengers1.append(n-1)
                else:
                    passengers2.append(n-1)
            else:
                passengers2.append(n-1)
        if syst.l2.direction==1 and syst.l1.direction==-1:
            if p.start>=syst.l2.currentfloor:
                passengers2.append(n-1)
            elif p.start<syst.l2.currentfloor and p.start>syst.l1.currentfloor:
                if p.dir=='u':
                    passengers1.append(n-1)
                else:
                    passengers2.append(n-1)
            else:
                passengers1.append(n-1)
        if syst.l2.direction==1 and syst.l1.direction==1:
            if p.start>=syst.l2.currentfloor:
                passengers2.append(n-1)
            elif p.start<syst.l2.currentfloor and p.start>syst.l1.currentfloor:
                if p.dir=='u':
                    passengers1.append(n-1)
                else:
                    passengers2.append(n-1)
            else:
                passengers2.append(n-1)
        if syst.l2.direction==-1 and syst.l1.direction==-1:
            if p.start>=syst.l2.currentfloor:
                passengers1.append(n-1)
            elif p.start<syst.l2.currentfloor and p.start>syst.l1.currentfloor:
                if p.dir=='u':
                    passengers1.append(n-1)
                else:
                    passengers2.append(n-1)
            else:
                passengers1.append(n-1)
    if syst.l1.direction==0 :
        passengers1.append(n-1)
    elif syst.l2.direction==0:
        passengers2.append(n-1)


def getpassengers(inp):
    k = -1
    r1 = 0
    r2 = 0
    for j in range(len(inp)):
        if inp[j]=='u' or inp[j]=='d'or inp[j]=='U' or inp[j]=='D':
            k = j
    if inp[0]!='-':
        if inp[k+1]!='-':
            for j in range(k):
                r1 = 10*r1 + int(inp[j])
            for j in range(k+1,len(inp)):
                r2 = 10*r2 + int(inp[j])
            p = passenger(r1,inp[k],r2)
            passengers.append(p)
        else:
            for j in range(k):
                r1 = 10*r1 + int(inp[j])
            for j in range(k+2,len(inp)):
                r2 = 10*r2 + int(inp[j])
            p = passenger(r1,inp[k],-r2)
            passengers.append(p)
    else:
        if inp[k+1]!='-':
            for j in range(1,k):
                r1 = 10*r1 + int(inp[j])
            for j in range(k+1,len(inp)):
                r2 = 10*r2 + int(inp[j])
            p = passenger(-r1,inp[k],r2)
            passengers.append(p)
        else:
            for j in range(1,k):
                r1 = 10*r1 + int(inp[j])
            for j in range(k+2,len(inp)):
                r2 = 10*r2 + int(inp[j])
            p = passenger(-r1,inp[k],-r2)
            passengers.append(p)
    waiting.append(len(passengers)-1)
    distributep()

def updatepas(q):
    msg =  pickle.loads(c.recv(1024))
        # print(msg)
    if msg == "q":
        pass
    else:
        getpassengers(msg)
    if q ==1:
        return passengers1
    else:
        return passengers2
    
def operate(l,pas,q,inlift=[]):
    while len(pas)==0:
        pas = updatepas(q)
        sleep(1)

    while passengers[pas[0]].start!=l.currentfloor:
        
        if passengers[pas[0]].start-l.currentfloor<0:
            l.fsm.transition("todown")
        elif passengers[pas[0]].start-l.currentfloor>0:
            l.fsm.transition("toup")

        l.fsm.execute()
        if q==2:
            print("                                                       ",end=" ")
        print(f"Lift {q}",end=" ")
        l.move()
    
    l.fsm.transition("torest")
    l.fsm.execute()

    if q==2:
        print("                                                       ",end=" ")
    print(f"Lift {q}",end=" ")
    l.move()
    if q==2:
        print("                                                       ",end=" ")
    print(f"Lift {q}",end=" ")
    print(f"HI passenger {pas[0]}")
   
    while passengers[pas[0]].end!=l.currentfloor:
        
        if passengers[pas[0]].end-l.currentfloor<0:
            l.fsm.transition("todown")
        elif passengers[pas[0]].end-l.currentfloor>0:
            l.fsm.transition("toup")

        l.fsm.execute()
        if q==2:
            print("                                                       ",end=" ")
        print(f"Lift {q}",end=" ")
        l.move()

    l.fsm.transition("torest")
    l.fsm.execute()
    if q==2:
        print("                                                       ",end=" ")
    print(f"Lift {q}",end=" ")
    l.move()
    if q==2:
        print("                                                       ",end=" ")
    print(f"Lift {q}",end=" ")
    print(f"BYE passenger {pas[0]}")
    if q==1:
        passengers1.pop(0)
        operate(l,passengers1,q)
    else:
        passengers2.pop(0)
        operate(l,passengers2,q)

passengers1 = []
passengers2 = []

if __name__ == '__main__':

    syst = system()
    syst.l1.fsm.states["rest"] = rest()
    syst.l1.fsm.states["up"] = up()
    syst.l1.fsm.states["down"] = down()
    syst.l1.fsm.transitions["torest"] = transistion("rest")
    syst.l1.fsm.transitions["toup"] = transistion("up")
    syst.l1.fsm.transitions["todown"] = transistion("down")

    syst.l2.fsm.states["rest"] = rest()
    syst.l2.fsm.states["up"] = up()
    syst.l2.fsm.states["down"] = down()
    syst.l2.fsm.transitions["torest"] = transistion("rest")
    syst.l2.fsm.transitions["toup"] = transistion("up")
    syst.l2.fsm.transitions["todown"] = transistion("down")    

    passengers = []
    waiting = []
    inlift1 = []
    inlift2= []
    # reached1 = []
    reached = []

    msg = "q"
    while msg == "q":
        msg = pickle.loads(c.recv(1024))
    getpassengers(msg)
    # print(passengers[0].start,passengers[0].dir,passengers[0].end,waiting)

    t1 = Thread(target=operate,args=[syst.l1,passengers1,1])
    t2 = Thread(target=operate,args=[syst.l2,passengers2,2])
    t1.start()
    t2.start()

    t1.join()
    t2.join()