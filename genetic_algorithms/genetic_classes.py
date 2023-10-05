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
        self.gen = 0
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

class NoneGE(IGeneticAlgorithm):
        
    def __init__(self,mapa):
        super().__init__(mapa)


    def population_generation_func(self) -> list[Individuo]:
        ind = Individuo([self.map.startPoint, self.map.startPoint],0)
        ind.score = 0
        return [ind]

    def selection_func(self) -> list[Individuo]:
        return self.population

    def cross_func(self, selected_pop) -> list[Individuo]:
        pass

    def mutation_func(self, crossed_pop) -> list[Individuo]:
        pass
    
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        return self.population

    def stop_func(self) -> bool:
        return True

    def display_func(self) -> None:
        #Console display at the end of the cycle.
        pass

class ElasticRopeGE(IGeneticAlgorithm):

    def __init__(self, start_population_size, stop_gen, converge_gens, cross_prob, cross_method, mutation_prob, mutation_traslation_radius, max_mutations_per_ind, mutation_method, point_distance, map_size_order, map):
        super().__init__(map)
        self.start_population_size = start_population_size
        self.stop_gen = stop_gen
        self.point_distance = point_distance
        self.map_size_order = map_size_order
        self.converge_gens = converge_gens
        self.cross_prob = cross_prob
        self.cross_method = cross_method
        self.mutation_prob = mutation_prob
        self.mutation_traslation_radius = mutation_traslation_radius
        self.max_mutations_per_ind = max_mutations_per_ind
        self.mutation_method = mutation_method
        
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

        fixing_start_individuals = [] 
        start_individuals =[] 
        first_individual = Individuo([self.map.startPoint,self.map.endPoint], 0)
        first_indiv_cols = self.map.getIndividualCollisions(first_individual)
        

        fixing_start_individuals.append((first_individual, first_indiv_cols))

        for _ in range(10):
            
            path =[self.map.startPoint] 

            for _ in range(random.randint(1,15)):
                x = round(random.random()*self.map.width, self.map_size_order)
                y = round(random.random()*self.map.height, self.map_size_order)

                path.append(Point(x,y))
            
            path.append(self.map.endPoint)

            indiv = Individuo(path,0) 
            cols = self.map.getIndividualCollisions(indiv)
            if(len(cols)>0):
                fixing_start_individuals.append((indiv,cols))
            else:
                start_individuals.append(indiv)
        start_individuals.extend(self.calculate_factibles(fixing_start_individuals, self.start_population_size))
 
        print("Start with: ", len(start_individuals))
        return start_individuals

    def selection_func(self) -> list[Individuo]:
        #No discriminamos, no filtramos ninguno
        return self.population

    def cross_func_1(self, selected_pop) -> list[Individuo]:
        #Elegimos dos individuos al azar (puede ser el mismo)
        crossed = []
        selected_pop_set = set(selected_pop)
        crossing_prob = 0
        for ind1 in selected_pop:
            if random.random() < crossing_prob:
                ind2 = random.choice(selected_pop)

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
                    ind = Individuo(son_path,self.gen)
                    ind.score = ind.calcLongitude()
                    print("Crossed?")
                    if ind not in selected_pop_set:
                        crossed.append(ind)
                    else:
                        print("duplicated!")

        return crossed
    
    def cross_func_2(self, selected_pop) -> list[Individuo]:
        selected_pop_set = set(selected_pop)
        crossed_sons = []

        for ind1 in selected_pop:
            if random.random() < self.cross_prob:
                ind2 = random.choice(selected_pop)
                ind1_path = ind1.getPath()
                ind2_path = ind2.getPath()
                ind1_point = random.randint(1,len(ind1_path)-2)
                ind2_point = random.randint(1,len(ind2_path)-2)
                
                son_path = [p.copy() for p in ind1_path[0:ind1_point]]
                son_path.extend([p.copy() for p in ind2_path[ind2_point:]])
                
                if len(set(son_path)) == len(son_path):
                    son = Individuo(son_path, self.gen)
                    son_collisions = self.map.getIndividualCollisions(son)
                    if(len(son_collisions)>0):
                        #Curamos al hijo
                        factible_sons = self.calculate_factibles([(son, son_collisions)], 4)
                        for s in factible_sons:
                            s.score = s.calcLongitude()
                            crossed_sons.append(s)
                    else:
                        son.score = son.calcLongitude()
                        crossed_sons.append(son)
        
        return crossed_sons

    def cross_func(self, selected_pop) -> list[Individuo]:

        if int(self.cross_method) == 1:
            return self.cross_func_1(selected_pop)
        else:
            return self.cross_func_2(selected_pop)


   #Selection of the mutation algorithm 
    def mutation_func(self, crossed_pop:list[Individuo]) -> list[Individuo]:
        if int(self.mutation_method) == 1:
            return self.mutation_func_1(crossed_pop)
        else:
            return self.mutation_func_2(crossed_pop)
    

   #Mutación por eliminación de un numero aleatorio puntos
    def mutation_func_1(self, crossed_pop:list[Individuo]) -> list[Individuo]:
        #Elminación de puntos
        mutation_list = [p for p in self.population]
        mutation_list.extend([p for p in crossed_pop])
        mutated = []

        maxErasingPoints = 1

        for i,ind in enumerate(mutation_list):

            if random.random() < self.mutation_prob:
                n_deletions = int(random.random()*(maxErasingPoints) +1)

                for _ in range(n_deletions):

                    if ind.getPathLength() > 2:
                        selected_ind = Individuo(ind.getPath(),self.gen)
                        selected_ind.erasePoint(random.randint(1, selected_ind.getPathLength()-2))

                        #Si no es factible, lo reparamos
                        ind_colls = self.map.getIndividualCollisions(selected_ind)
                        if len(ind_colls) > 0:
                            fixes = self.calculate_factibles([(mutation_list[i],ind_colls)],1)
                            if len(fixes) > 0:
                                #print("Mutated!")
                                mutated.append(fixes[0])

                        #Una vez tenemos un individuo factible, calculamos su puntuación
                        selected_ind.score = selected_ind.calcLongitude()
                    else:
                        break
                    
        return mutated

    
    def mutation_func_2(self, crossed_pop:list[Individuo]) -> list[Individuo]:
        mutation_list = [p for p in self.population]
        mutation_list.extend([p for p in crossed_pop])
        mutated = []

        for i,ind in enumerate(mutation_list):

            if random.random() < self.mutation_prob:
    
                n_translations = int(random.random()*(self.max_mutations_per_ind) +1)
                
                path = ind.getPath()

                for _ in range(n_translations):
                    
                    point_index = random.randint(1, len(path)-2)
                    point = path[point_index]

                    new_x = round(min(max((random.random()*2-1)*self.mutation_traslation_radius + point.x, 1), self.map.width-1), self.map_size_order)
                    new_y = round(min(max((random.random()*2-1)*self.mutation_traslation_radius + point.y, 1), self.map.height-1), self.map_size_order)
                    path[point_index] = Point(new_x, new_y)

                selected_ind = Individuo(path, self.gen)
                #Si no es factible, lo reparamos
                ind_colls = self.map.getIndividualCollisions(selected_ind)
                if len(ind_colls) > 0:
                    fixes = self.calculate_factibles([(mutation_list[i],ind_colls)],1)
                    if len(fixes) > 0:
                        #print("Mutated!")
                        mutated.append(fixes[0])

                    #Una vez tenemos un individuo factible, calculamos su puntuación
                    selected_ind.score = selected_ind.calcLongitude()
                else:
                    selected_ind.score = selected_ind.calcLongitude()
                    mutated.append(selected_ind)

        return mutated



    
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        #Nos quedamos con el mismo tamaño: la población inicial.
        replaced = []
        replaced.extend(selected)
        replaced.extend(crossed_pop)
        replaced.extend(mutated_pop)
        print("sel",len(selected),len(crossed_pop),len(mutated_pop))

        replaced.sort(key=(lambda i: i.score))
        replaced = replaced[:self.start_population_size]
        return replaced

    def stop_func(self) -> bool:
        #Paramos cuando la solución no mejore en 40 generaciones
        return self.gen - self.fittest.gen >= self.converge_gens or self.gen >= self.stop_gen

    def display_func(self) -> None:
        if self.fin:
            print("END - Fittest fount at generation ", self.gen,"with score of",self.fittest.score)
            print(f"The path has {self.fittest.getPathLength()} points")
        else:
            print(f"Generation {self.gen} Fittest: {round(self.fittest.score,2)} Converge condition: {self.gen - self.fittest.gen}/{self.converge_gens}")
