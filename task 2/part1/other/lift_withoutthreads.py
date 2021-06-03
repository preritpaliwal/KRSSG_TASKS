# states
from threading import Thread
from time import time

class rest():
    def __init__(self):
        self.state = "rest"
    def execute(self):
        print("passengers pass leave or enter the lift...it is at rest")


class up():
    def __init__(self):
        self.state = "up"
    def execute(self):
        print("traveling up")


class down():
    def __init__(self):
        self.state = "down"
    def execute(self):
        print("traveling down")


# =================================================================================


class transistion():
    def __init__(self,tostate):
        self.tostate = tostate

    def execute(self):
        print("transistioning...")


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

    # def changedir(self,i):
    #     self.direction = i
    #     print("hi")

    # def move(self):
    #     self.currentfloor +=self.direction
    #     print("bye")
    def move(self):
        print(f"from {self.currentfloor}",end=" ")
        if(self.fsm.curstate.state=="up"):
            self.currentfloor+=1
        if(self.fsm.curstate.state=="down"):
            self.currentfloor+=(-1)
        if(self.fsm.curstate.state=="rest"):
            self.currentfloor+=0
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
    for p in pas:
        print(p.start,p.end)
        # print(p.start-syst.l1.currentfloor)
        print("\n====================================================================\n")
        while p.start-l.currentfloor != 0:
            print(q)
            if p.start-l.currentfloor>0:
                l.fsm.transition("toup")
            else:
                l.fsm.transition("todown")
            l.fsm.execute()
            l.move()

        print(q)
        l.fsm.transition("torest")
        l.fsm.execute()
        l.move()

        while p.end-l.currentfloor != 0:
            print(q)
            if p.end-l.currentfloor>0:
                l.fsm.transition("toup")
            else:
                l.fsm.transition("todown")
            l.fsm.execute()
            l.move()

        print(q)
        l.fsm.transition("torest")
        l.fsm.execute()
        l.move()

        print("\n====================================================================\n")

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
            if inputs[i][j]=='u' or inputs[i][j]=='d':
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
    # t1.start()
    # t2.start()

    # t1.join()
    # t2.join()
    # print(time()-s)
    for p in passengers1:
        print(p.start,p.end)
        # print(p.start-syst.l1.currentfloor)
        print("\n====================================================================\n")
        while p.start-syst.l1.currentfloor != 0:
            if p.start-syst.l1.currentfloor>0:
                syst.l1.fsm.transition("toup")
            else:
                syst.l1.fsm.transition("todown")
            syst.l1.fsm.execute()
            syst.l1.move()

        syst.l1.fsm.transition("torest")
        syst.l1.fsm.execute()
        syst.l1.move()

        while p.end-syst.l1.currentfloor != 0:
            if p.end-syst.l1.currentfloor>0:
                syst.l1.fsm.transition("toup")
            else:
                syst.l1.fsm.transition("todown")
            syst.l1.fsm.execute()
            syst.l1.move()

        syst.l1.fsm.transition("torest")
        syst.l1.fsm.execute()
        syst.l1.move()

        print("\n====================================================================\n")

    print("\n\n\nlift 2\n\n\n")
    for p in passengers2:
        # print(p.start-syst.l2.currentfloor)
        print(p.start,p.end)
        print("\n====================================================================\n")
        while p.start-syst.l2.currentfloor != 0:
            if p.start-syst.l2.currentfloor>0:
                syst.l2.fsm.transition("toup")
            else:
                syst.l2.fsm.transition("todown")
            syst.l2.fsm.execute()
            syst.l2.move()

        syst.l2.fsm.transition("torest")
        syst.l2.fsm.execute()
        syst.l2.move()

        while p.end-syst.l2.currentfloor != 0:
            if p.end-syst.l2.currentfloor>0:
                syst.l2.fsm.transition("toup")
            else:
                syst.l2.fsm.transition("todown")
            syst.l2.fsm.execute()
            syst.l2.move()

        syst.l2.fsm.transition("torest")
        syst.l2.fsm.execute()
        syst.l2.move()

        print("\n====================================================================\n")

    print(time()-s)