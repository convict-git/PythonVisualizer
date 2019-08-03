import numpy as np
import os
import Queue
import heapq

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

dxd = [-1, 0, 1]
dyd = [0, -1, 1]

NORM='\033[0m'
BLACK='\033[40m'
RED='\033[41m'
BLUE='\033[42m'
GREEN='\033[44m'
GRAY='\033[47m'

class environment:
	 def __init__(self, n, olist):
			self.n = n
			self.ctr = 0
			N = n*n
			k = N//5
			obsList = np.random.choice(N, k, replace=False)
			# obsList = []
			# for i in range(len(olist)):
			#   obsList.append(olist[i][0]*self.n + olist[i][1])

			self.obstacle = set(obsList)     #set for obstacles
			self.vis = [0 for i in range(N)] #list of visited
			self.Par = [(-1, -1) for i in range(N)] #Parent pointers
			self.Path = set()
			self.ok = False

	 def validMove(self, x, y, px, py):
			if (x < 0 or y < 0 or x >= self.n or y >= self.n):
				 return False
			elif (x is px and y is py):
				 return False
			elif (self.vis[self.n*x + y] == 1):
				 return False
			elif ((self.n*x + y) in self.obstacle):
				 return False
			else:
				 return True

	 def show(self, cx, cy):
			os.system("sleep 0.04")
			os.system("clear")
			for i in range(self.n):
				 s = ''
				 for j in range(self.n):
						if i is cx and j is cy:
							 s = s + str(RED + '  ' + NORM)
						elif self.n*i + j in self.Path:
							 s = s + str(GREEN + '  ' + NORM)
						elif self.n*i + j in self.obstacle:
							 s = s + str(BLACK + '  ' + NORM)
						elif self.vis[self.n*i + j] is 1:
							 s = s + str(BLUE + '  ' + NORM)
						else:
							 s = s + str(GRAY + '  ' + NORM)
				 print(s)
			print("Total Iterations: " + str(self.ctr))

	 def clear(self):
			self.Par = [(-1, -1) for i in range(self.n*self.n)] #Parent pointers
			self.vis = [0 for i in range(self.n*self.n)] #Parent pointers
			self.ctr = 0

	 def printPath(self, sx, sy, tx, ty):
			ctr = 0
			ii, jj = tx, ty
			while (ii is not sx or jj is not sy):
				 ctr += 1
				 self.show(ii, jj)
				 print((ii, jj), self.Par[self.n*ii + jj])
				 self.Path.add(self.n*ii + jj)
				 ii, jj = self.Par[self.n*ii + jj]
			self.Path.add(self.n*sx + sy)
			self.show(sx, sy)
			print(ctr)

	 def dfs(self, sx, sy, tx, ty, px, py):
			self.vis[self.n*sx + sy] = 1
			self.show(sx, sy)
			self.ctr += 1
			if self.ok is True:
				 return
			if (sx == tx and sy == ty):
				 self.ok = True
				 return
			for ii in range(4):
				 Sx = sx + dx[ii]
				 Sy = sy + dy[ii]
				 if (self.validMove(Sx, Sy, px, py) == True and self.vis[self.n*Sx + Sy] == 0):
						self.Par[self.n*Sx + Sy] = self.n*Sx + Sy
						self.dfs(Sx, Sy, tx, ty, sx, sy)

	 def bfs(self, sx, sy, tx, ty):
			if (self.n*sx + sy in self.obstacle):
				 self.obstacle.remove(self.n*sx + sy)
			if (self.n*tx + ty in self.obstacle):
				 self.obstacle.remove(self.n*tx + ty)
			self.clear()
			q = Queue.Queue()
			inf = 100000
			d = [inf for i in range(self.n*self.n)]
			d[self.n*sx + sy] = 0
			self.vis[self.n*sx + sy] = 1
			q.put((sx, sy))

			while (q.empty() == False):
				 self.ctr += 1
				 ux, uy = q.get()
				 self.show(ux, uy)
				 if (ux is tx and uy is ty):
						break

				 for ii in range(4):
						Sx, Sy = ux + dx[ii], uy + dy[ii]
						if (self.validMove(Sx, Sy, ux, uy) == True):
							 if (d[self.n*Sx + Sy] > d[self.n*ux + uy] + 1):
									self.vis[self.n*Sx + Sy] = 1
									d[self.n*Sx + Sy] = d[self.n*ux + uy] + 1
									q.put((Sx, Sy))
									self.Par[self.n*Sx + Sy] = (ux, uy)

			self.printPath(sx, sy, tx, ty)

	 def dist(self, x1, y1, x2, y2):
			return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

	 def astar(self, sx, sy, tx, ty):
			if (self.n*sx + sy in self.obstacle):
				 self.obstacle.remove(self.n*sx + sy)
			if (self.n*tx + ty in self.obstacle):
				 self.obstacle.remove(self.n*tx + ty)
			self.clear()
			inf = 100000
			d = [inf for i in range(self.n*self.n)]
			d[self.n*sx + sy] = 0
			self.vis[self.n*sx + sy] = 1
			frontier = []
			heapq.heappush(frontier, [self.dist(sx, sy, tx, ty) + 0, sx, sy]);

			while(True):
				 self.ctr += 1
				 ds, ux, uy = heapq.heappop(frontier)
				 self.show(ux, uy)
				 if (ux is tx and uy is ty):
						break

				 for ii in range(3):
						for jj in range(3):
							 if (dxd[ii] is 0 and dyd[jj] is 0):
									continue
							 Sx, Sy = ux + dxd[ii], uy + dyd[jj]
							 if (self.validMove(Sx, Sy, ux, uy) == True):
										 if (d[self.n*Sx + Sy] > d[self.n*ux + uy] + 1):
												self.vis[self.n*Sx + Sy] = 1
												d[self.n*Sx + Sy] = d[self.n*ux + uy] + 1
												heapq.heappush(frontier, [self.dist(Sx, Sy, tx, ty) + d[self.n*Sx + Sy], Sx, Sy])
												self.Par[self.n*Sx + Sy] = (ux, uy)

			self.printPath(sx, sy, tx, ty)

inp = raw_input().split()
for i in range(len(inp)):
	 inp[i] = int(inp[i])

sx, sy, tx, ty = inp
tc = int(raw_input())
obs = []
while (tc > 0):
	 tc-=1
	 u, v = raw_input().split()
	 u, v = int(u), int(v)
	 obs.append((u, v))

e1 = environment(20, obs)
e2 = environment(20, obs)
e1.bfs(sx, sy, tx, ty)
os.system("sleep 2")
e2.astar(sx, sy, tx, ty)
