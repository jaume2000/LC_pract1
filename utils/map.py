from utils.math_lines import Line, Point
from utils.indiviuo import Individuo

class Map :
    def __init__(self, width, height, startPoint:Point, endPoint:Point, obstacleLines:list[Line]=[]):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstacles = obstacleLines
        self.width = width
        self.height = height

    def addObstacle(self,obs:Line):
        self.obstacles.append(obs)

    def getIntersections(self, l:Line, printInters=False):

        res =  list(filter(lambda obs: l.intersect_lines(obs), self.obstacles))
        if(printInters):
            print("Intesercted lines:")
            for l in res:
                print(str(l))
        return tuple(res)
    
    def getIndividualCollisions(self, indiv:Individuo)->tuple[(int,Line)]:

        res = []
        path = indiv.getPath()
        
        for i in range(len(path)-1):
            intersections = self.getIntersections(Line(path[i].x,path[i].y, path[i+1].x,path[i+1].y))
            if len(intersections)>0:
                res.append( (i, intersections) )
        return tuple(res)
    
    def isIndividualFactible(self, indiv:Individuo)->bool:

        path = indiv.getPath()
        i = 0
        while i < len(path)-1:
            intersections = self.getIntersections(Line(path[i].x,path[i].y, path[i+1].x,path[i+1].y))
            if len(intersections)>0:
                return False
            i+=1
        return True

    def pointInsideMap(self, p:Point):
        return 0 < p.x < self.width and 0 < p.y < self.height
