import sys
sys.path.append('../')

from abc import abstractmethod
from abc import ABCMeta
from utils.indiviuo import Individuo
from utils.map import Map
from utils.math_lines import Point, Line, Vector
import random
import math

class IGeneticAlgorithm(metaclass=ABCMeta):

    def __init__(
            self,
            map:Map
    ):
        self.map = map
        self.population = []
        self.fittest = None
        self.gen = 0;
        self.fin = False
    
    def orderPopulation(self):
        self.population.sort(key=(lambda i: i.score))
        if self.fittest == None or self.fittest.score > self.population[0].score:
            self.fittest = self.population[0].copy()

    def start(self):
        self.fin = False
        self.population = self.population_generation_func()
        self.orderPopulation()
        self.display_func()
        while not self.fin:
            selected = self.selection_func()
            crossed = self.cross_func(selected)
            mutated = self.mutation_func(crossed)
            self.population = self.replace_func(selected, crossed, mutated)
            self.orderPopulation()
            self.fin = self.stop_func()
            self.display_func()

            self.gen+=1
        

    @abstractmethod
    def population_generation_func(self) -> list[Individuo]:
        #self.map
        #IMPORTANT TO SET the indiviaul.score!
        #Returns the list of initial individuals
        pass

    @abstractmethod
    def selection_func(self) -> list[Individuo]:
        # Returns a subset of the individuals.
        # If you return null or empty list, the algorithm won't work. You are depatching all individuals.
        # If you want to do nothing here, return self.population.
        pass

    @abstractmethod
    def cross_func(self, selected_pop) -> list[Individuo]:
        # If you return null or empty list, the algorithm won't work. You are depatching all individuals.
        # If you want to do nothing here, return selected_pop.
        pass

    @abstractmethod
    def mutation_func(self, crossed_pop) -> list[Individuo]:
        # If you return null or empty list, the algorithm won't work. You are depatching all individuals.
        # If you want to do nothing here, return crossed_pop.
        pass
    
    @abstractmethod
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        pass

    @abstractmethod
    def stop_func(self) -> bool:
        pass

    @abstractmethod
    def display_func(self) -> None:
        #Console display at the end of the cycle.
        pass


class PrintingGE(IGeneticAlgorithm):
    def __init__(self):
        print("Creating the generator")
        super().__init__(None)

    def population_generation_func(self) -> list[Individuo]:
        print("Generating population...")
        pass

    def selection_func(self) -> list[Individuo]:
        print("Selecting")
        return []

    def cross_func(self, selected_pop) -> list[Individuo]:
        print("Crossing")
        return []

    def mutation_func(self, crossed_pop) -> list[Individuo]:
        print("Muttating")
        return []
    
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        print("Replacing")
        return []

    def stop_func(self) -> bool:
        return self.gen >= 10

    def display_func(self) -> None:
        print("DISPLAYING!!! " + str(self.gen))

class RandomGE(IGeneticAlgorithm):
    def __init__(self, population_size, max_indiv_size, max_gen, rand_radius, mapa):
        super().__init__(mapa)

        self.population_size = population_size
        self.max_indiv_size = max_indiv_size
        self.rand_radius = rand_radius
        self.max_gen = max_gen
    
    def calc_score(self, indiv:Individuo):
        indiv.calcLongitude()
        intersections_punishment = 10**len(self.map.getIndividualCollisions(indiv)[1])
        indiv.score *= intersections_punishment
        return 


    def population_generation_func(self) -> list[Individuo]:
        print("Generating " + str(self.population_size))
        population = []
        for i in range(self.population_size):
            indiv = Individuo([self.map.startPoint],self.gen)

            for j in range(self.max_indiv_size):
                x = random.randint(1,self.map.width)
                y = random.randint(1,self.map.height)
                indiv.addPoint(Point(x,y))

            indiv.addPoint(self.map.endPoint)
            self.calc_score(indiv)
            
            population.append(indiv)
        return population

    def selection_func(self) -> list[Individuo]:
        #Selección elitista del top 20%
        selected = self.population[0:round(len(self.population)*0.75)]
        return selected

    def cross_func(self, selected_pop) -> list[Individuo]:
        return selected_pop

    def mutation_func(self, crossed_pop) -> list[Individuo]:
        mutated = []
        mutation_prob = 1
        i = 0
        totals = len(crossed_pop)
        while totals < self.population_size*1.5:
            if random.random() < mutation_prob:
                path = self.population[i].getPath()
                rand_index = random.randint(1, len(path)-2)

                x = min(max(round(path[rand_index].x + (random.random()*2-1)*self.rand_radius), 1), self.map.width-1)
                y = min(max(round(path[rand_index].y + (random.random()*2-1)*self.rand_radius), 1), self.map.height-1)
                path[rand_index] = Point(x,y)
                indiv = Individuo(path, self.gen, True)
                
                self.calc_score(indiv)

                mutated.append(indiv)

                totals+=1
            i=( i+1 )% len(crossed_pop)

        return mutated
    
    def replace_func(self, selected:list[Individuo], crossed_pop:list[Individuo], mutated_pop:list[Individuo]) -> list[Individuo]:
        selected.extend(mutated_pop)
        return selected

    def stop_func(self) -> bool:
        if self.gen >= self.max_gen:
            print("FIN")
        return self.gen >= self.max_gen 

    def display_func(self) -> None:
        print("Fittest of the gen " + str(self.gen) + ": "+ str(self.fittest.score), "Size", len(self.population))

class ElasticRopeGE(IGeneticAlgorithm):

    def __init__(self, start_population_size, stop_gen, point_distance, map_size_order, map):
        super().__init__(map)
        self.start_population_size = start_population_size
        self.stop_gen = stop_gen
        self.point_distance = point_distance
        self.map_size_order = map_size_order
        
    def calculate_factibles(self, non_factible_list:list[(Individuo,tuple)], n_solutions):
        
        need_fix = non_factible_list.copy()
        factible_solutions = []

        def algorithm(translated_point,changed_path):
                if self.map.pointInsideMap(translated_point) and translated_point not in changed_path:
                    changed_path.insert(colls[0][0]+1, translated_point)

                    indiv = Individuo(changed_path, self.gen)
                    #print(ind, "\t| Added at ", colls[0][0]+1,"|", indiv)
                    #print("Collision info", colls)
                    next_colls = self.map.getIndividualCollisions(indiv)
                    if len(next_colls) > 0:
                        
                        #print("Pushed path", indiv)
                        need_fix.append((indiv,next_colls))
                    else:
                        #print("Acepted factible solution", indiv)
                        indiv.score = indiv.calcLongitude()
                        factible_solutions.append(indiv)
        
        def calculate_individual1(collided_line):
            changed_path = ind.getPath()
            move_vector = -Vector.round(collided_line.u * (self.point_distance), self.map_size_order)
            translated_point = Point(collided_line.p1.x + move_vector.x, collided_line.p1.y + move_vector.y)
            algorithm(translated_point,changed_path)
        
        def calculate_individual2(collided_line):
            changed_path = ind.getPath()
            move_vector = Vector.round(collided_line.u * (self.point_distance), self.map_size_order)
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

                move_vector = Vector.round(ortogonals[0] * (self.point_distance), self.map_size_order)

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

    def population_generation_func(self) -> list[Individuo]:
        #self.map
        #IMPORTANT TO SET the indiviaul.score!!!!

        first_individual = Individuo([self.map.startPoint,self.map.endPoint], 0)
        first_indiv_cols = self.map.getIndividualCollisions(first_individual)
        if(len(first_indiv_cols)==0):
            return [first_individual]

        start_individuals = self.calculate_factibles([(first_individual, first_indiv_cols)], self.start_population_size)
 
        print("Start with: ", len(start_individuals))
        return start_individuals

    def selection_func(self) -> list[Individuo]:
        #No discriminamos, no filtramos ninguno
        return self.population

    def cross_func(self, selected_pop) -> list[Individuo]:
        #Elegimos dos individuos al azar (puede ser el mismo)

        crossed = []
        crossing_prob = 0.1
        for ind1 in self.population:
            for ind2 in self.population:
                if random.random() < crossing_prob:
                    ind1 = self.population[random.randint(0, len(self.population)-1)]
                    ind2 = self.population[random.randint(0, len(self.population)-1)]
                    # A partir de un punto al azar,
                    # buscamos un punto en común entre los dos caminos, del cual el siguiente punto tenga que ser diferente.
                    ind1_path = ind1.getPath()
                    ind2_path = ind2.getPath()

                    point1_index = random.randint(1,len(ind1_path)-2)
                    point1 = ind1_path[point1_index]
                    point2_index = 1
                    while point2_index < len(ind2_path) and ind2_path[point2_index] != point1:
                        point2_index+=1
                    
                    #Si el punto común no es el último, mezclamos
                    if point2_index < len(ind2_path)-2:
                        son_path = [p.copy() for p in ind1_path[:point1_index]]
                        for p in ind2_path[point2_index:]:
                            son_path.append(p.copy())
                        crossed.append(Individuo(son_path,self.gen))

        return crossed

    def mutation_func(self, crossed_pop:list[Individuo]) -> list[Individuo]:
        #Elminación de puntos
        prob_erasing = 1
        mutation_list = [p for p in self.population]
        mutation_list.extend([p for p in crossed_pop])
        mutated = []
        for i,ind in enumerate(mutation_list):
            if ind.getPathLength() > 2 and random.random() < prob_erasing:
                selected_ind = ind.copy()
                selected_ind.erasePoint(random.randint(1, selected_ind.getPathLength()-2))

                #Si no es factible, lo reparamos
                ind_colls = self.map.getIndividualCollisions(selected_ind)
                if len(ind_colls) > 0:
                    fixes = self.calculate_factibles([(mutation_list[i],ind_colls)],1)
                    if len(fixes) > 0:
                        #print("Mutated!")
                        mutated.append(fixes[0])
                #Una vez tenemos un individuo factible, calculamos su puntuación
                selected_ind.score = ind.calcLongitude()
        return mutated
    
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        #Nos quedamos con el mismo tamaño: la población inicial.
        replaced = []
        replaced.extend(selected)
        replaced.extend(crossed_pop)
        replaced.extend(mutated_pop)
        print(len(selected),len(crossed_pop),len(mutated_pop))

        replaced.sort(key=(lambda i: i.score))
        replaced = replaced[:self.start_population_size]
        return replaced

    def stop_func(self) -> bool:
        #Paramos cuando la solución no mejore en 40 generaciones
        return self.gen - self.fittest.gen >= 40 or self.gen >= self.stop_gen

    def display_func(self) -> None:
        if self.fin:
            print("END - Fittest fount at generation ", self.gen,"with score of",self.fittest.score)
        else:
            print("Generation",self.gen, "Fittest:", self.fittest.score)
