from functools import reduce
from utils.math_lines import Line

class Individuo:

    def __init__(self, lines:list):
        self.lines = lines

    def calcLongitude(self):
        return reduce(lambda x,y: x+y.calc_distance(), self.lines,0)
    
    def getPath(self):
        return self.lines

#print(Individuo([Line(0,0,0,1),Line(0,1,1,0)]).calcLongitude())   # Devuelve 2.4142