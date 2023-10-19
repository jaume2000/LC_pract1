import sys
sys.path.append('../')

from utils.indiviuo import Individuo
from utils.math_lines import Point, Line, Vector
import random


def calculate_factibles(map, gen, point_distance, map_size_order, non_factible_list:list[(Individuo,tuple)], n_solutions):
    
    need_fix = non_factible_list.copy()
    factible_solutions = []

    def algorithm(translated_point,changed_path):
            if map.pointInsideMap(translated_point) and translated_point not in changed_path:
                changed_path.insert(colls[0][0]+1, translated_point)

                indiv = Individuo(changed_path, gen)
                #print(ind, "\t| Added at ", colls[0][0]+1,"|", indiv)
                #print("Collision info", colls)
                next_colls = map.getIndividualCollisions(indiv)
                if len(next_colls) > 0:
                    
                    #print("Pushed path", indiv)
                    need_fix.append((indiv,next_colls))
                else:
                    #print("Acepted factible solution", indiv)
                    indiv.score = indiv.calcLongitude()
                    factible_solutions.append(indiv)
    
    def calculate_individual1(collided_line):
        changed_path = ind.getPath()
        move_vector = -Vector.round(collided_line.u * (point_distance), map_size_order)
        translated_point = Point(collided_line.p1.x + move_vector.x, collided_line.p1.y + move_vector.y)
        algorithm(translated_point,changed_path)
    
    def calculate_individual2(collided_line):
        changed_path = ind.getPath()
        move_vector = Vector.round(collided_line.u * (point_distance), map_size_order)
        translated_point = Point(collided_line.p2.x + move_vector.x, collided_line.p2.y + move_vector.y)
        algorithm(translated_point,changed_path)

    while(len(need_fix)>0 and len(factible_solutions) < n_solutions):
    
        # For all the individuals that need a fix:
        (ind,colls) = need_fix.pop()
            #In the first section, we select the list of collisions and then choose the first collision.

        i = 0
        changed_path = ind.getPath()
        collided_line = colls[0][1][i]
        collision_segment = Line(changed_path[colls[0][0]].x,changed_path[colls[0][0]].y, changed_path[colls[0][0]+1].x,changed_path[colls[0][0]+1].y)

        while collided_line.v.ortogonals()[0] * collision_segment.v == 0 and i < len(colls[0][1])-1:
            i+=1
            collided_line = colls[0][1][i]
            

        #Si la colisión es de dos segmentos que están en la misma linea, pillamos el punto más cercano de la colisión y añadimos al path dos opciones: por arriba y por abajo.
        collision_segment = Line(changed_path[colls[0][0]].x,changed_path[colls[0][0]].y, changed_path[colls[0][0]+1].x,changed_path[colls[0][0]+1].y)
        if collided_line.v.ortogonals()[0] * collision_segment.v == 0:
            ortogonals = collided_line.u.ortogonals()

            move_vector = Vector.round(ortogonals[0] * (point_distance), map_size_order)

            translated_point = Point(collided_line.p1.x + move_vector.x, collided_line.p1.y + move_vector.y)
            algorithm(translated_point,changed_path)

            changed_path = ind.getPath()
            translated_point = Point(collided_line.p2.x + move_vector.x, collided_line.p2.y + move_vector.y)
            algorithm(translated_point,changed_path)

            move_vector = -move_vector

            changed_path = ind.getPath()
            translated_point = Point(collided_line.p1.x + move_vector.x, collided_line.p1.y + move_vector.y)
            algorithm(translated_point,changed_path)

            changed_path = ind.getPath()
            translated_point = Point(collided_line.p2.x + move_vector.x, collided_line.p2.y + move_vector.y)
            algorithm(translated_point,changed_path)

            pass
        else:
            if random.random() < 0.5:
                calculate_individual1(collided_line)
                calculate_individual2(collided_line)
            else:
                calculate_individual2(collided_line)
                calculate_individual1(collided_line)
        
        #End while

    return factible_solutions
