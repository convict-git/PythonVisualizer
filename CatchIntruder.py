import os
import numpy as np
GREEN_F='\033[42m'
BOLD='\033[1m'
NORM='\033[0m'
RED_F='\033[41m'
GREY='\033[47m'
YELLOW='\033[43m'
BLUE='\033[44m'

class Defence:
    Array = []
    n = 0
    k = 0
    initIntrPos = [0, 0]
    path = set()
    def __init__(self, n, posx, posy, k):
        self.n = n
        self.k = k
        for i in range(self.n):
            for j in range(self.n):
                self.Array.append(0)
        self.initIntrPos = [posx, posy]
        self.path.add(self.n*posx + posy)

    def getNextPos(self):
        ok = False
        X = 0
        Y = 0
        D = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        while ok is False:
            d = np.random.choice(4)
            X = D[d][0]
            Y = D[d][1]
            curX = self.initIntrPos[0]
            curY = self.initIntrPos[1]
            if (curX + X == self.initIntrPos[0] and curY + Y == self.initIntrPos[1]):
                ok = False
                continue

            if (curX + X < 0 or curX + X >= self.n or curY + Y < 0 or curY + Y >= self.n):
                ok = False
            else:
                ok = True

        self.initIntrPos[0] = self.initIntrPos[0] + X
        self.initIntrPos[1] = self.initIntrPos[1] + Y
        self.path.add(self.n*self.initIntrPos[0] + self.initIntrPos[1])

    def changeSensor(self):
        N = self.n*self.n
        K = self.k
        sensorList = np.random.choice(N, K, replace=False)
        sensorList.sort()

        for i in range(self.n):
            for j in range(self.n):
                self.Array[self.n*i + j] = 0
        for it in sensorList:
            self.Array[it] = 1

    def show(self):
        for i in range(self.n):
            s = ''
            for j in range(self.n):
                X = self.initIntrPos[0]
                Y = self.initIntrPos[1]
                if i is X and j is Y:
                    if self.Array[self.n*i + j] is 1:
                        s = s + str(BOLD+BLUE+'  '+NORM)
                    else:
                        s = s + str(BOLD+GREEN_F+'  '+NORM)
                    #print(BOLD+GREEN_F+' '+NORM),
                elif self.Array[self.n*i + j] is 1:
                    s = s + str(YELLOW+'  '+NORM)
                    #print(YELLOW+' '+NORM),
                else:
                    if self.n*i + j in self.path:
                        s = s + str(BOLD+RED_F+'  '+NORM)
                        #print(BOLD+RED_F+' '+NORM),
                    else:
                        s = s + str(GREY+'  '+NORM)
                        #print(GREY+' '+NORM),
            print(s)

    def findIntruder(self):
        x = self.initIntrPos[0]
        y = self.initIntrPos[1]
        if self.Array[self.n*x + y] == 1:
            return True
        else:
            return False


def main():
    N = int(raw_input("Enter N :"))
    posx = int(raw_input("Enter x of intruder: "))
    posy = int(raw_input("Enter y of intruder: "))
    k = int(raw_input("Enter k: "))
    d = Defence(N, posx, posy, k)
    numberOfStep = 1
    ok = False
    while ok is False:
        d.changeSensor()
        d.show()
        ok = d.findIntruder()
        if ok is True:
            print("Found")
            print('Time ', numberOfStep)
            print('Location of Intruder', d.initIntrPos)
            break
        else:
            print("Not found")
            numberOfStep = numberOfStep + 1
        d.getNextPos()
        os.system("sleep .08")
        os.system("clear")

if __name__ == "__main__":
    main()
