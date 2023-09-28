from functools import reduce
from utils.math_lines import Line, Point

class Individuo:

    def __init__(self, points:list[Point], gen=0, calcScore:bool=False):
        self.__points = points
        self.gen = gen
        self.score = None
        if calcScore:
            self.calcLongitude()

    def __str__(self) -> str:
        res = "(Path: "
        for p in self.__points:
            res+= "("+str(p.x)+", "+str(p.y)+") ->"
        return res
    
    def __hash__(self) -> int:
        return hash(tuple(self.__points))

    def calcLongitude(self):
        sum = 0
        for i in range(len(self.__points)-1):
            sum += Line.calc_distance_from_points(self.__points[i], self.__points[i+1])
        self.score = sum
        return sum
    
    def getPath(self):
        return self.__points.copy()
    
    def getPathLength(self):
        return len(self.__points)
    
    def erasePoint(self, i):
        if 0 < i < len(self.__points):
            del self.__points[i]
    
    def addPoint(self, p:Point):
        self.__points.append(p)
    def hasRepeatedPoints(self):
        return len(set(self.__points)) != len(self.__points)
    
    def copy(self):
        ind = Individuo([p.copy() for p in self.__points], self.gen)
        ind.score = self.score
        return ind
    
    

#print(Individuo([Line(0,0,0,1),Line(0,1,1,0)]).calcLongitude())   # Devuelve 2.4142