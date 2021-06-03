# states
from threading import Thread
from time import time
import numpy as np

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
        

class system():
    def __init__(self):
        self.l1 = lift()
        self.l2 = lift()


class passenger():
    def __init__(self,start,dir,end):
        self.start = start
        self.dir = dir
        self.end = end


def operate(l,pas,q):
    if len(pas)==0:
        print(f"\n\nNO Passenger for lift {q}\n\ndistance moved = {l.distance}")
        return
    pstart = []
    pend = []
    n = len(pas)
    for i in range(n):
        pstart.append((pas[i].start,i))
        pend.append((pas[i].end,i))

    pstart.sort()
    pend.sort()

    waiting = []
    inlift = []
    reached = []
    for i in range(len(pas)):
        waiting.append(i)
    
    if q==1:
        l.direction = 1
        while(pstart[n-1][0]!=l.currentfloor):
            print(f"Lift {q}")
            if pstart[n-1][0]-l.currentfloor<0:
                l.fsm.transition("todown")
            elif pstart[n-1][0]-l.currentfloor>0:
                l.fsm.transition("toup")
            for e in inlift:
                if pas[e].end == l.currentfloor:
                    l.fsm.transition("torest")
                    print(f"BYE passenger {e}")
                    reached.append(e)
                    inlift.remove(e)
            
            for w in waiting:
                if pas[w].start == l.currentfloor:
                    if np.sign(pas[w].end-l.currentfloor)==l.direction:
                        l.fsm.transition("torest")
                        print(f"HI passenger {w}")
                        inlift.append(w)
                        waiting.remove(w)
            l.fsm.execute()
            l.move()
        
        print(f"Lift {q}")
        for w in range(n):
            if pas[w].start == pstart[n-1][0] and (np.sign(pend[n-1][0]-l.currentfloor)==np.sign(pas[w].end-l.currentfloor) or np.sign(pend[n-1][0]-l.currentfloor)==0):
                waiting.remove(w)
                inlift.append(w)
                print(f"HI passemnger {w}")
                l.fsm.transition("torest")
                l.fsm.execute()
                l.move()

        if pend[n-1][0]>=l.currentfloor:
            while pend[n-1][0]!=l.currentfloor:
                print(f"Lift {q}")
                l.fsm.transition("toup")
                for e in inlift:
                    if pas[e].end==l.currentfloor:
                        l.fsm.transition("torest")
                        print(f"BYE passenger {e}")
                        reached.append(e)
                        inlift.remove(e)
                l.fsm.execute()
                l.move()

            for  e in range(len(pas)):
                if pas[e].end == pend[n-1][0]:
                    print(f"Lift {q}")
                    inlift.remove(e)
                    reached.append(e)
                    print(f"BYE passemnger {e}")
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    l.move()
        
        while pend[0][0]!=l.currentfloor and len(reached)!=n:
            print(f"Lift {q}")
            l.fsm.transition("todown")

            for e in inlift:
                if pas[e].end == l.currentfloor:
                    l.fsm.transition("torest")
                    print(f"BYE passenger {e}")
                    reached.append(e)
                    inlift.remove(e)
            
            for w in waiting:
                if pas[w].start == l.currentfloor:
                    if np.sign(pas[w].end-l.currentfloor)==l.direction:
                        l.fsm.transition("torest")
                        print(f"HI passenger {w}")
                        inlift.append(w)
                        waiting.remove(w)
            l.fsm.execute()
            l.move()
        
        if len(reached)!=n:
            for e in range(len(pas)):
                if pas[e].end==pend[0][0]:
                    print(f"Lift {q}")
                    print(f"Bye passenger {e}")
                    inlift.remove(e)
                    reached.append(e)
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    l.move()

    if q==2:
        l.direction = -1
        while(pstart[0][0]!=l.currentfloor):
            if pstart[0][0]-l.currentfloor<0:
                l.fsm.transition("todown")
            elif pstart[0][0]-l.currentfloor>0:
                l.fsm.transition("toup")

            for e in inlift:
                if pas[e].end == l.currentfloor:
                    l.fsm.transition("torest")
                    print(f"                                                                  Lift {q}",end=" ")
                    print(f"BYE passenger {e}")
                    reached.append(e)
                    inlift.remove(e)
            
            for w in waiting:
                if pas[w].start == l.currentfloor:
                    if np.sign(pas[w].end-l.currentfloor)==l.direction:
                        l.fsm.transition("torest")
                        print(f"                                                                  Lift {q}",end=" ")
                        print(f"HI passenger {w}")
                        inlift.append(w)
                        waiting.remove(w)
            print(f"                                                                  Lift {q}",end=" ")
            l.fsm.execute()
            l.move()

        for w in range(n):
            if pas[w].start == pstart[0][0] and (np.sign(pend[0][0]-l.currentfloor)==np.sign(pas[w].end-l.currentfloor) or np.sign(pend[0][0]-l.currentfloor)==0):
                waiting.remove(w)
                inlift.append(w)
                print(f"                                                                  Lift {q}",end=" ")
                print(f"HI passemnger {w}")
                l.fsm.transition("torest")
                l.fsm.execute()
                print(f"                                                                  Lift {q}",end=" ")
                l.move()

        if pend[0][0]<=l.currentfloor:
            while pend[0][0]!=l.currentfloor:
                l.fsm.transition("todown")
                for e in inlift:
                    if pas[e].end==l.currentfloor:
                        l.fsm.transition("torest")
                        print(f"                                                                  Lift {q}",end=" ")
                        print(f"BYE passenger {e}")
                        reached.append(e)
                        inlift.remove(e)
                print(f"                                                                  Lift {q}",end=" ")
                l.fsm.execute()
                l.move()

            for e in range(len(pas)):
                if pas[e].end == pend[0][0]:
                    inlift.remove(e)
                    reached.append(e)
                    print(f"                                                                  Lift {q}",end=" ")
                    print(f"BYE passemnger {e}")
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    print(f"                                                                  Lift {q}",end=" ")
                    l.move()
        
        while pend[n-1][0]!=l.currentfloor and len(reached)!=n:
            l.fsm.transition("toup")

            for e in inlift:
                if pas[e].end == l.currentfloor:
                    l.fsm.transition("torest")
                    print(f"                                                                  Lift {q}",end=" ")
                    print(f"BYE passenger {e}")
                    reached.append(e)
                    inlift.remove(e)
            
            for w in waiting:
                if pas[w].start == l.currentfloor:
                    if np.sign(pas[w].end-l.currentfloor)==l.direction:
                        l.fsm.transition("torest")
                        print(f"                                                                  Lift {q}",end=" ")
                        print(f"HI passenger {w}")
                        inlift.append(w)
                        waiting.remove(w)
            print(f"                                                                  Lift {q}",end=" ")
            l.fsm.execute()
            l.move()
        if len(reached)!=n:
            for e in range(len(pas)):
                if pas[e].end==pend[n-1][0]:
                    print(f"                                                                  Lift {q}",end=" ")
                    print(f"Bye passenger {e}")
                    inlift.remove(e)
                    reached.append(e)
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    print(f"                                                                  Lift {q}",end=" ")
                    l.move()


    if len(reached)==len(pas)==n and len(waiting)==len(inlift)==0:
        print(f"\n\nWORK is DONE by lift {q}!!!\n\n distance by {q}th lift is {l.distance}\n\n\n")

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


    inputs = []
    while True:
        inp = input()
        if inp == "":
            break
        inputs.append(inp)

    passengers = []
    for i in range(len(inputs)):
        k = -1
        r1 = 0
        r2 = 0
        for j in range(len(inputs[i])):
            if inputs[i][j]=='u' or inputs[i][j]=='d'or inputs[i][j]=='U' or inputs[i][j]=='D':
                k = j
        if inputs[i][0]!='-':
            if inputs[i][k+1]!='-':
                for j in range(k):
                    r1 = 10*r1 + int(inputs[i][j])
                for j in range(k+1,len(inputs[i])):
                    r2 = 10*r2 + int(inputs[i][j])
                p = passenger(r1,inputs[i][k],r2)
                passengers.append(p)
            else:
                for j in range(k):
                    r1 = 10*r1 + int(inputs[i][j])
                for j in range(k+2,len(inputs[i])):
                    r2 = 10*r2 + int(inputs[i][j])
                p = passenger(r1,inputs[i][k],-r2)
                passengers.append(p)
        else:
            if inputs[i][k+1]!='-':
                for j in range(1,k):
                    r1 = 10*r1 + int(inputs[i][j])
                for j in range(k+1,len(inputs[i])):
                    r2 = 10*r2 + int(inputs[i][j])
                p = passenger(-r1,inputs[i][k],r2)
                passengers.append(p)
            else:
                for j in range(1,k):
                    r1 = 10*r1 + int(inputs[i][j])
                for j in range(k+2,len(inputs[i])):
                    r2 = 10*r2 + int(inputs[i][j])
                p = passenger(-r1,inputs[i][k],-r2)
                passengers.append(p)

    guu,gud,gdd,gdu = [],[],[],[]
    guustart,gudstart,gddstart,gdustart= [],[],[],[]
    guuend,gudend,gddend,gduend= [],[],[],[]

    for p in passengers:
        print(p.start,p.dir,p.end)
        if p.start>=0 and p.dir=='u':
            guu.append(p)
            guuend.append((p.end,len(guu)-1))
            guustart.append((p.start,len(guu)-1))
        elif p.start>0 and p.dir=='d':
            gud.append(p)
            gudend.append((p.end,len(gud)-1))
            gudstart.append((p.start,len(gud)-1))
        elif p.start<=0 and p.dir=='u':
            gdu.append(p)
            gduend.append((p.end,len(gdu)-1))
            gdustart.append((p.start,len(gdu)-1))
        else:
            gdd.append(p)
            gddend.append((p.end,len(gdd)-1))
            gddstart.append((p.start,len(gdd)-1))

    guustart.sort()
    gudstart.sort()
    gddstart.sort()
    gdustart.sort()
    guuend.sort()
    gudend.sort()
    gddend.sort()
    gduend.sort()

    if len(guu)==0:
        guustart.append((0,0))
        guuend.append((0,0))
    if len(gud)==0:
        gudstart.append((0,0))
        gudend.append((0,0))
    if len(gdd)==0:
        gddstart.append((0,0))
        gddend.append((0,0))
    if len(gdu)==0:
        gdustart.append((0,0))
        gduend.append((0,0))
    
    factor1 = 2*gudstart[-1][0] - min(gddend[0][0],gudend[0][0])  -  (2*max(guuend[-1][0],gudstart[-1][0]) - gudend[0][0])
    factor2 = -2*gdustart[0][0] + max(guuend[-1][0],gduend[-1][0])  -  (2*max(-gddend[0][0],-gdustart[0][0]) + gduend[-1][0])

    print(factor1,factor2)

    
    passengers1 = []
    passengers2 = []

    if factor1+factor2>=0:
        for p in guu:
            passengers1.append(p)
        for p in gud:
            passengers1.append(p)
        for p in gdu:
            passengers2.append(p)
        for p in gdd:
            passengers2.append(p)
    else:
        for p in guu:
            passengers2.append(p)
        for p in gud:
            passengers1.append(p)
        for p in gdu:
            passengers2.append(p)
        for p in gdd:
            passengers1.append(p)
    
    t1 = Thread(target=operate,args=[syst.l1,passengers1,1])
    t2 = Thread(target=operate,args=[syst.l2,passengers2,2])
    s = time()
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print(time()-s)