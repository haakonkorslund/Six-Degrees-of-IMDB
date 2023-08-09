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
