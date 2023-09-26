from utils.math_lines import Line, Point
from utils.indiviuo import Individuo

class Map :
    def __init__(self, width, height, startPoint:Point, endPoint:Point, obstacleLines:list[Line]=[]):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.obstacles = obstacleLines
        self.width = width
        self.height = height

        self.obstacles.append(Line(0,0, 0,width))
        self.obstacles.append(Line(0,width, height,width))
        self.obstacles.append(Line(height,width, height, 0))
        self.obstacles.append(Line(height,0, 0,0))

    def addObstacle(self,obs:Line):
        self.obstacles.append(obs)

    def getIntersections(self, l:Line, printInters=False):

        res =  list(filter(lambda obs: l.intersect_lines(obs), self.obstacles))
        if(printInters):
            print("Intesercted lines:")
            for l in res:
                print(str(l))
        return tuple(res)
    
    def getIndividualCollisions(self, indiv:Individuo)->list[(int,Line)]:

        res = []
        path = indiv.getPath()
        
        for i in range(len(path)-1):
            intersections = self.getIntersections(Line(path[i].x,path[i].y, path[i+1].x,path[i+1].y))
            
            if len(intersections)>0:
                res.append( (i, intersections) )
        return tuple(res)

    def pointInsideMap(self, p:Point):
        return 0 < p.x < self.width and 0 < p.y < self.height
