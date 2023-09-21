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

    def calcLongitude(self):
        sum = 0
        for i in range(len(self.__points)-1):
            sum += Line.calc_distance_from_points(self.__points[i], self.__points[i+1])
        self.score = sum
        return sum
    
    def getPath(self):
        return self.__points.copy()
    
    def addPoint(self, p:Point):
        self.__points.append(p)
    
    

#print(Individuo([Line(0,0,0,1),Line(0,1,1,0)]).calcLongitude())   # Devuelve 2.4142