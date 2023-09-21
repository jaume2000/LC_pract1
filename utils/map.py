from utils.math_lines import Line, Point

class Map :
    def __init__(self, width, height, startPoint:Point, endPoint:Point, obstacleLines:list=[]):
        self.start = startPoint
        self.endPoint = endPoint
        self.obstacles = obstacleLines

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
        return res
    
