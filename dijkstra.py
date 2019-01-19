import os
import sys
import numpy as np

dx = [0, -1, 1, 0]
dy = [1, 0, 0, -1]

GREEN = '\033[42m'  # visited
BLACK = '\033[40m'  # obstacle
NORM = '\033[0m'
RED = '\033[41m'  # path
GREY = '\033[47m'  # background screen
BLUE = '\033[44m'  # target and source


class graph:

    def __init__(self, n, m):
        self.rows = n
        self.columns = m
        N = n*m
        k = N//4
        obstaclesList = np.random.choice(N, k, replace=False)
        obstaclesList.sort()
        self.obstacle = set(obstaclesList)

    def allowed(self, cX, dX, cY, dY):
        nX = cX + dX
        nY = cY + dY
        if nX < 0 or nX >= self.rows or nY < 0 or nY >= self.columns:
            return False
        else:
            if self.rows*nX + nY in self.obstacle:
                return False
            else:
                return True

    def show(self, source, target, found, vis, path):
        os.system("printf \"\033c\"")

        for row in range(self.rows):
            s = ''
            for col in range(self.columns):
                if row is source[0] and col is source[1]:
                    s = s + str(BLUE + '  ' + NORM)
                elif row is target[0] and col is target[1]:
                    s = s + str(BLUE + '  ' + NORM)
                elif self.rows*row + col in self.obstacle:
                    s = s + str(BLACK + '  ' + NORM)
                elif found is True and path[row][col] is 1:
                    s = s + str(RED + '  ' + NORM)
                elif vis[row][col] is 1:
                    s = s + str(GREEN + '  ' + NORM)
                else:
                    s = s + str(GREY + '  ' + NORM)
            print(s)

        os.system("sleep 0.01")

    def dijkstra(self, source, target):
        vis = [[0 for c in range(self.columns)] for r in range(self.rows)]
        dist = [[sys.maxint for c in range(self.columns)] for r in range(self.rows)]
        parent = [[(0, 0) for c in range(self.columns)] for r in range(self.rows)]
        path = [[0 for c in range(self.columns)] for r in range(self.rows)]

        # remove source from obstacle if found
        if self.rows*source[0] + source[1] in self.obstacle:
            self.obstacle.remove(self.rows*source[0] + source[1])

        # remove target from obstacle if found
        if self.rows*target[0] + target[1] in self.obstacle:
            self.obstacle.remove(self.rows*target[0] + target[1])

        for i in range(self.rows * self.columns):
            minX = 0
            minY = 0
            minD = sys.maxint
            dist[source[0]][source[1]] = 0

            # get the min from heap
            for r in range(self.rows):
                for c in range(self.columns):
                    if vis[r][c] is 0:
                        if minD > dist[r][c]:
                            minD = dist[r][c]
                            minX = r
                            minY = c

            vis[minX][minY] = 1
            if minX is target[0] and minY is target[1]:
                break

            # relax neighbouring edges
            canGo = False
            for it in range(4):
                nX = minX + dx[it]
                nY = minY + dy[it]
                if self.allowed(minX, dx[it], minY, dy[it]) is True:
                    canGo = True
                    if vis[nX][nY] is 0 and dist[nX][nY] > dist[minX][minY] + 1:
                        dist[nX][nY] = dist[minX][minY] + 1
                        parent[nX][nY] = (minX, minY)
            self.show(source, target, False, vis, path)

            if canGo is False:
                break

        if canGo is False:
            print("I'm stuck. No possible Path")
            return sys.maxint
        else:
            # generate path
            cX = parent[target[0]][target[1]][0]
            cY = parent[target[0]][target[1]][1]

            while True:
                if cX is source[0] and cY is source[1]:
                    break
                path[cX][cY] = 1
                cX = parent[cX][cY][0]
                cY = parent[cX][cY][1]

            self.show(source, target, True, vis, path)

            return dist[target[0]][target[1]]

'''
        for r in range(self.rows):
            s = ''
            for c in range(self.columns):
                if path[r][c] is 1:
                    s = s + str(1)
                else:
                    s = s + str(0)
            print(s)
'''


def main():
    n, m, sX, sY, tX, tY = [int(inp) for inp in raw_input().split()]
    g = graph(n, m)
    g.dijkstra([sX, sY], [tX, tY])


if __name__ == "__main__":
    main()
