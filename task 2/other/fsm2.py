from random import randint
from time import time

# ========================================================

class lighton():
    def __init__(self):
        pass
    def execute(self):
        print("light is on")


class lightoff():
    def __init__(self):
        pass
    def execute(self):
        print("light is off")

#==========================================================

class transistion():
    def __init__(self,tostate):
        self.tostate = tostate

    def execute(self):
        print("transistioning...")

class simplefsm():
    def __init__(self,char):
        self.char = char 
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
    

# =========================================================

class char():
    def __init__(self):
        self.fsm = simplefsm(self)
        self.lighton = True

# =========================================================

if __name__ == '__main__':
    light = char()
    light.fsm.states["on"] = lighton()
    light.fsm.states["off"] = lightoff()
    light.fsm.transitions["toon"] = transistion('on')
    light.fsm.transitions["tooff"] = transistion("off")

    light.fsm.setstate("on")

    # print(light.fsm.states)

    for i in range(20):
        starttime = time()        
        timeinterval = 0
        while(starttime+timeinterval>time()):
            pass
        if(randint(0,2)):
            if(light.lighton):
                light.fsm.transition("tooff")
                light.lighton = False
            else:
                light.fsm.transition("toon")
                light.lighton = True
        light.fsm.execute()