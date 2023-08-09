from cmath import inf
from collections import defaultdict
from node import Node
from film import Film
from heapq import heappush, heappop

class Graph:
    def __init__(self):
        self.nodesdict = {}
        self.filmdict = {}

    def addNode(self,name,id,f):
        n = Node(name,id,f)
        self.nodesdict[n.id] = n
        return n

    def print_graph(self):
	    for key in sorted(list(self.nodesdict.keys())):
		    print(key +str(self.nodesdict[key].neighbours))
    
    def getEdges(self):
        edge = 0
        for key in self.nodesdict:
            edge += len(self.nodesdict[key].neighbours)
        return edge //2

    def makeFilm(self,id,name,rate,votes):
        f = Film(id,name,rate,votes)
        self.filmdict[f.id] = f
        return f
                    
    def findPath(self,start,target):
        found = False
        explored = set()
        explored.add(start)
        stack = []
        stack += self.nodesdict[start].neighbours
        
        for n in self.nodesdict[start].neighbours:
            self.nodesdict[n[0]].parent = [start,n[1]]
            explored.add(n[0])
        
        while len(stack)>=1 and not found:
            u = stack.pop(0)
            for n in self.nodesdict[u[0]].neighbours:
                if n[0] not in explored:
                    self.nodesdict[n[0]].parent = [u[0],n[1]]
                    explored.add(n[0])
                    stack.append(n)
                    
                    if n[0] == target:
                        found = True
                        break
        
        self.nodesdict[start].parent = None
        p = self.nodesdict[target].parent
        pathlist = []
        pathlist.append([self.filmdict[p[1]].name,self.filmdict[p[1]].rate, self.nodesdict[p[0]].name])
        
        while self.nodesdict[p[0]].parent is not None:
            p = self.nodesdict[p[0]].parent
            pathlist.append([self.filmdict[p[1]].name,self.filmdict[p[1]].rate, self.nodesdict[p[0]].name])
        pathlist.reverse()
        path = ""
        for a in pathlist:
            path += a[2] + " === [ "
            path += a[0] + " ("
            path += a[1]
            path += ") ] ===> "
        path += self.nodesdict[target].name
        print(path)

        return

    def findChillPath(self, start, target):
        queue = [(0,start)]
        dist = defaultdict(lambda:float("inf"))
        dist[start] = 0
        parents = {start : None}
        found = False
    
        while queue and not found:
            cost, v = heappop(queue)
            for u in self.nodesdict[v].neighbours:
                a = 10 - float(self.filmdict[u[1]].rate)
                c = cost + a
                if c < dist[u[0]]:
                    self.nodesdict[u[0]].parent = [v,u[1]]
                    parents[u[0]] = v
                    dist[u[0]] = c
                    heappush(queue,(c,u[0]))
                    
        
            
        if target in dist.keys():
            weight = 0
            ant = 1
            self.nodesdict[start].parent = None
            p = self.nodesdict[target].parent
            pathlist = []
            weight+= 10 - float(self.filmdict[p[1]].rate)
            pathlist.append([self.filmdict[p[1]].name,self.filmdict[p[1]].rate, self.nodesdict[p[0]].name])
            
            while self.nodesdict[p[0]].parent is not None:
                p = self.nodesdict[p[0]].parent
                weight+= 10 - float(self.filmdict[p[1]].rate)
                pathlist.append([self.filmdict[p[1]].name,self.filmdict[p[1]].rate, self.nodesdict[p[0]].name])
            pathlist.reverse()
            path = ""
            for a in pathlist:
                path += a[2] + " === [ "
                path += a[0] + " ("
                path += a[1]
                path += ") ] ===> "
            path += self.nodesdict[target].name
            print(path)
            print("Total Weight: "+ str(ant*weight))
            return
                
        print("Path not found")
    
    
    def allComponents(self):
        self.comps = defaultdict(lambda:int(0))
        visited = set()
        
        for key in self.nodesdict.keys():
            size = 1
            queue = []
            
            if key not in visited:
                visited.add(key)
                if len(self.nodesdict[key].neighbours) == 0:
                    self.comps[size] = self.comps[size]+1
                else:
                    for node in self.nodesdict[key].neighbours:
                        if node[0] not in visited:
                            size+=1
                            queue.append(node)
                            visited.add(node[0])
                            while len(queue)>=1:
                                u = queue.pop(0)
                                for n in self.nodesdict[u[0]].neighbours:
                                    if n[0] not in visited:
                                        size+=1
                                        visited.add(n[0])
                                        queue.append(n)
                                
                    self.comps[size] = self.comps[size]+1
    
    def getComp(self,size):
        print("There are "+ str(self.comps[size]) +" components of size "+str(size))