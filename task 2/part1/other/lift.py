# states
from threading import Thread
from time import time
import numpy as np

class rest():
    def __init__(self):
        self.state = "rest"
    def execute(self):
        # print("passengers pass leave or enter the lift...it is at rest")
        pass


class up():
    def __init__(self):
        self.state = "up"
    def execute(self):
        # print("traveling up")
        pass


class down():
    def __init__(self):
        self.state = "down"
    def execute(self):
        # print("traveling down")
        pass


# =================================================================================


class transistion():
    def __init__(self,tostate):
        self.tostate = tostate

    def execute(self):
        # print("transistioning...")
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
        start = time()
        while start+1>time():
            pass
        
        


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
            # print(inlift)
            for  e in range(len(pas)):
                if pas[e].end == pend[n-1][0]:
                    print(f"Lift {q}")
                    inlift.remove(e)
                    reached.append(e)
                    print(f"BYE passemnger {e}")
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    l.move()
            # print(inlift)
        
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
            print(f"Lift {q}---->>>>",end=" ")
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

        print(f"Lift {q}---->>>>",end=" ")
        for w in range(n):
            if pas[w].start == pstart[0][0] and (np.sign(pend[0][0]-l.currentfloor)==np.sign(pas[w].end-l.currentfloor) or np.sign(pend[0][0]-l.currentfloor)==0):
                waiting.remove(w)
                inlift.append(w)
                print(f"HI passemnger {w}")
                l.fsm.transition("torest")
                l.fsm.execute()
                l.move()

        if pend[0][0]<=l.currentfloor:
            while pend[0][0]!=l.currentfloor:
                print(f"Lift {q}---->>>>",end=" ")
                l.fsm.transition("todown")
                for e in inlift:
                    if pas[e].end==l.currentfloor:
                        l.fsm.transition("torest")
                        print(f"BYE passenger {e}")
                        reached.append(e)
                        inlift.remove(e)
                l.fsm.execute()
                l.move()

            for e in range(len(pas)):
                if pas[e].end == pend[0][0]:
                    print(f"Lift {q}---->>>>",end=" ")
                    inlift.remove(pend[0][1])
                    reached.append(pend[0][1])
                    print(f"BYE passemnger {pend[0][1]}")
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    l.move()
        
        while pend[n-1][0]!=l.currentfloor and len(reached)!=n:
            print(f"Lift {q}---->>>>",end=" ")
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
        if len(reached)!=n:
            for e in range(len(pas)):
                if pas[e].end==pend[n-1][0]:
                    print(f"Lift {q}---->>>>",end=" ")
                    print(f"Bye passenger {e}")
                    inlift.remove(e)
                    reached.append(e)
                    l.fsm.transition("torest")
                    l.fsm.execute()
                    l.move()


    if len(reached)==len(pas)==n and len(waiting)==len(inlift)==0:
        print(f"\n\nWORK is DONE by lift {q}!!!\n\n distance by {q}th lift is {l.distance}\n\n\n")

if __name__ == '__main__':
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



    for p in passengers:
        print(p.start,p.dir,p.end)

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

    passengers1 = []
    passengers2 = []

    for p in passengers:
        if p.start<0:
            passengers2.append(p)
        elif p.start>0:
            passengers1.append(p)
        else:
            if p.end>0:
                passengers1.append(p)
            else:
                passengers2.append(p)

    t1 = Thread(target=operate,args=[syst.l1,passengers1,1])
    t2 = Thread(target=operate,args=[syst.l2,passengers2,2])
    s = time()
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print(time()-s)