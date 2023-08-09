import csv
from cmath import inf
from collections import defaultdict
from heapq import heappush, heappop

class Film:
    def __init__(self, id, name, rate, votes) -> None:
        self.id = id
        self.name = name
        self.rate = rate
        self.votes = votes
        self.nodes = []


class Node:
    def __init__(self, name, id,films) -> None:
        self.name = name
        self.id = id
        self.films = films
        self.neighbours = []
        self.parent = None

    
    def addNeighbour(self,n,f):
        if n not in self.neighbours:
            self.neighbours.append((n,f))

    def exists(self,a,f):
        if (a,f) in self.appended or (f,a) in self.appended:
            return True
        else:
            self.appended.add((a,f))
            return False

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

def makeGraph(films, actors):
    g = Graph()
    makeFilmList(g,films)
    makeActorList(g,actors)

    return g
            
def makeActorList(g,actors):
    with open(actors, encoding="utf8") as actor:
        s = csv.reader(actor, delimiter="\t")
        for x in s:
            id = x[0]
            name = x[1]
            aFilms = []
            i = 2
            while i < len(x):
                if x[i] in g.filmdict:
                    g.filmdict[x[i]].nodes.append(id)
                aFilms.append(x[i])
                i += 1
            g.addNode(name,id,aFilms)
        
        for key in g.nodesdict.keys():
            for f in g.nodesdict[key].films:
                if f in g.filmdict:
                    for node in g.filmdict[f].nodes:
                        g.nodesdict[key].neighbours.append([node,f])
                    g.nodesdict[key].neighbours.remove([key,f])
    return 

def makeFilmList(g,films):
    with open(films, encoding="utf8") as film:
        f = csv.reader(film, delimiter="\t")
        for x in f:
            id = x[0]
            name = x[1]
            rate = x[2]
            votes = x[3]
            g.makeFilm(id,name,rate,votes)

    return


def stats(graph):
    print("Nodes: "+str(len(graph.nodesdict)))
    print("Edges: "+str(graph.getEdges()))

def main():
    g= makeGraph("movies.tsv","actors.tsv")
    print("Oppgave 1 \n")
    stats(g)
    print("Oppgave 2\n")
    print("Paths:\n")
    print("---------")
    g.findPath("nm2255973", "nm0000460")
    print("---------")
    g.findPath("nm0424060","nm0000243")
    print("---------")
    g.findPath("nm4689420", "nm0000365")
    print("---------")
    g.findPath("nm0000288", "nm0001401")
    print("---------")    
    g.findPath("nm0031483","nm0931324")
    print("---------")
    print("\n")

    print("Oppgave 3\n")
    print("Chillest:\n")
    g.findChillPath("nm2255973", "nm0000460")
    print("---------")
    g.findChillPath("nm0424060","nm0000243")
    print("---------")
    g.findChillPath("nm4689420", "nm0000365")
    print("---------")
    g.findChillPath("nm0000288", "nm0001401")
    print("---------")    
    g.findChillPath("nm0031483","nm0931324")
    print("\n")
    g.allComponents()

    print("Oppgave 4\n")
    g.getComp(113102)
    g.getComp(11)
    g.getComp(10)
    g.getComp(9)
    g.getComp(8)
    g.getComp(7)
    g.getComp(6)
    g.getComp(5)
    g.getComp(4)
    g.getComp(3)
    g.getComp(2)
    g.getComp(1)

main()