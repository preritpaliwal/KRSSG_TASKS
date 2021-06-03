# Welcome to Hotel Transylvania
# 1 == Rest
# 0 == Up
# 2 == Down

def ready(inp, state):
    l = []
    m = []

    for i in inp:
        m.append(i[0])
        m.append(i[2])

    for i in m:
        if i not in l:
            l.append(i)
    
    if state == 0:
        for i in range(len(l)):
            for j in range(0,len(l)-i-1):
                if l[j]>l[j+1]:
                    l[j], l[j+1] = l[j+1],l[j]

    if state == 2:
        for i in range(len(l)):
            for j in range(0,len(l)-i-1):
                if l[j]<l[j+1]:
                    l[j], l[j+1] = l[j+1],l[j]
    return l 


class Lift:
    def __init__(self,curr_floor):
        self.currentf = curr_floor
        self.state = 1
        self.floor_stops = []
        self.last_state = 1
        self.mem_floors = [0]
    
    def go(self):
        if len(self.floor_stops) != 0:
            t = self.floor_stops.pop(0)
            self.currentf = t
            if t != self.mem_floors[-1]:
                self.mem_floors.append(t)

        else:
            self.state = 1

class LiftSystem:
    def __init__(self):
        self.lu = Lift(0)      # Change the 0 to any floor number of your choice.
        self.ld = Lift(0)      # Change the 0 to any floor number of your choice.
        # self.lu.state = 0
        self.lu.last_state = 2
        # self.ld.state = 2
        self.ld.last_state = 0
        self.lifts = [self.lu,self.ld]

    def operate(self,inp):
        for l in self.lifts:
            if l.state == 1:
                l.last_state = 2 - l.last_state
                l.state = l.last_state
                # print(l.state)
                # Code to put in the floor stops is to be put here
                # Idea is to seperate the input list which itself contains the data in form of lists having three elements i.e. take, state, drop into two lists of diff states
                # After that put the list with same state data as the state of lift
                # Also after putting all the stops duplicate floors are deleted and the floors are arranged descending or ascending on the basis of lift's state. 
                m = []
                for i in inp:
                    if l.state == 0:
                        if i[1] == 'U' and i[0]>=l.currentf:
                            m.append(i)
                            # m.append(i)
                            # inp.remove(i)
                            # n = ready(m,l.state)
                            # print(inp)
                    if l.state == 2:
                        if i[1] == 'D' and i[0]<=l.currentf:
                            m.append(i)
                            # inp.remove(i)
                            # n = ready(m,l.state)
                for j in m:
                    inp.remove(j)
                # print(m)
                n = ready(m,l.state)
                m.clear()
                # print(n)
                for i in n:
                    l.floor_stops.append(i)
                # print(l.floor_stops)
            else:
                l.go()


# Real Flow of the program 
inp = []
n = int(input("Enter the number of passengers i.e. number of entries: "))
while n:
    a = []
    a.append(int(input("Floor from where to pick up: ")))
    a.append(input("State of the flow i.e. either U or D: "))
    a.append(int(input("Floor where to drop: ")))
    inp.append(a)
    n -= 1

l = LiftSystem()
# print(inp)
l.operate(inp)

while len(inp) != 0 or len(l.lu.floor_stops) != 0 or len(l.ld.floor_stops) != 0:
    l.operate(inp)
    # print(inp)


print("Lift-1: ",l.lu.mem_floors)
print("Lift-2: ",l.ld.mem_floors)