
import math
class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        
    def __str__(self):
        return '('+str(self.x) + ', '+ str(self.y) +')'
        
    def __hash__(self):
        return hash((self.x,self.y))
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
class Vector:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.longitude = math.sqrt(self.x**2+self.y**2)

    def round(self,digits):
        return Vector(round(self.x, digits), round(self.y, digits))

    def normalize(self):
        return Vector(self.x / self.longitude, self.y / self.longitude)
    def __str__(self):
        return '('+str(self.x) + ', '+ str(self.y) +')'
    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def __sub__(self,other):
        return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
class Line: 

    def __str__(self):
        return 'P1: ' + str(self.p1) + ', P2: ' + str(self.p2) + ', y = x*' + str(self.m) + ' + ' + str(self.b)

    def __init__(self, x1,y1, x2,y2):

        self.p1 = Point(x1,y1)
        self.p2 = Point(x2,y2)
        self.v = Vector(x2-x1, y2-y1)
        self.u = self.v.normalize()
        self.m = (y2-y1)/(x2-x1) if x1-x2 != 0 else 'inf'
        self.b = y1 - x1*self.m if self.m != 'inf' else 'inf'

    def calc_distance(self):
        return math.sqrt((self.p1.x-self.p2.x)**2 + (self.p1.y-self.p2.y)**2)
    
    def calc_distance_from_points(p1:Point, p2:Point):
        return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

     
    def __check_point_inside_line_range(self, p:Point):
        value1 = (self.p1.y <= p.y <= self.p2.y or self.p2.y <= p.y <= self.p1.y)
        value2 = (self.p1.x <= p.x <= self.p2.x or self.p2.x <= p.x <= self.p1.x)
        return value1 and value2

    def intersect_lines(self, other):

        #Esta es una linea vertical
        if self.m == 'inf':
            #Ambas son verticales
            if other.m == 'inf':

                #Ambas líneas son verticales en la misma x. Hay que mirar si sus tramos intersecan.
                if self.p1.x == other.p1.x:
                    return self.__check_point_inside_line_range(other.p1) or self.__check_point_inside_line_range(other.p2) or other.__check_point_inside_line_range(self.p1) or other.__check_point_inside_line_range(self.p2)
                else:
                    return False
            #La otra no es vertical
            else:
                x = self.p1.x
                y = round(other.m*x + other.b, 10)
                p = Point(x,y)

                return self.__check_point_inside_line_range(p) and other.__check_point_inside_line_range(p)
                
        #La otra es una linea vertical y la nuestra no lo es
        elif other.m == 'inf':
            x = other.p1.x
            y = round(self.m*x + self.b, 10)
            p = Point(x,y)

            return other.__check_point_inside_line_range(p) and self.__check_point_inside_line_range(p)
        
        #Ninguna es vertical
        else:
            #Tienen la misma m
            if self.m == other.m:
                if self.b == other.b:
                    #Hay que comprobar si las rectas se intersecan.
                    return self.__check_point_inside_line_range(other.p1) or self.__check_point_inside_line_range(other.p2) or other.__check_point_inside_line_range(self.p1) or other.__check_point_inside_line_range(self.p2)
                #Son pararlelas, no intersecan
                else:
                    return False
            #Caso general, no tienen la misma pendiente, intersecarán si o si.
            else:
                #Punto de intersección
                x = round((other.b - self.b)/(self.m-other.m),5)
                y = round(self.m*x + self.b, 5)
                p = Point(x,y)
                #Hay que comprobar que el punto de intersección entra en los rangos de las líneas.
                return self.__check_point_inside_line_range(p) and other.__check_point_inside_line_range(p)
