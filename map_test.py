import os,sys
from utils.indiviuo import Individuo
from utils.math_lines import Line, Point
from utils.map import Map
sys.path.append('../')

with open('./datos.txt') as f:
    map_width, map_height = map(lambda x:int(x), f.readline().split())
    obstacles = [] 
    Map(100,100, Point(1,1), Point(10,10), []).getIntersections(Line(10,-10,10,100), True)
    Individuo([Line(0,0,10,10)])
    
