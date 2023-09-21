from functools import reduce
from utils.math_lines import Line

class Individuo:

    def __init__(self, points:list, gen=0):
        self.points = points
        self.gen = gen

    def calcLongitude(self):
        sum = 0
        for i in range(len(self.points)-1):
            sum += Line.calc_distance_from_points(self.points[i], self.points[i+1])
        return sum
    
    def getPath(self):
        return self.points
    

#print(Individuo([Line(0,0,0,1),Line(0,1,1,0)]).calcLongitude())   # Devuelve 2.4142