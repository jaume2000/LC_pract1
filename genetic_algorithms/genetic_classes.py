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
    
    def orderPopulation(self):
        self.population.sort(key=(lambda i: i.score))
        self.fittest = self.population[0]

    def start(self):
        fin = False
        self.population = self.population_generation_func()
        self.orderPopulation()
        self.display_func()
        while not fin:
            selected = self.selection_func()
            crossed = self.cross_func(selected)
            mutated = self.mutation_func(crossed)
            self.population = self.replace_func(selected, crossed, mutated)
            self.orderPopulation()
            self.display_func()
            fin = self.stop_func()

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

    def population_generation_func(self) -> list[Individuo]:
        #self.map
        #IMPORTANT TO SET the indiviaul.score!!!!

        start_individuals = []
        first_individual = Individuo([self.map.startPoint,self.map.endPoint])
        print(first_individual)
        first_indiv_cols = self.map.getIndividualCollisions(first_individual)
        if(len(first_indiv_cols)==0):
            return [first_individual]

        need_fix = {(first_individual, first_indiv_cols)}
        while(len(need_fix)>0):
            next_need_fix = set()

            # For all the individuals that need a fix:
            for (ind,colls) in need_fix:
                #In the first section, we select the list of collisions and then choose the first collision.
                collided_line = colls[0][1][0]
                

                def algorithm():
                    if self.map.pointInsideMap(translated_point) and translated_point not in changed_path:
                        changed_path.insert(colls[0][0]+1, translated_point)

                        indiv = Individuo(changed_path)
                        #print(ind, "\t| Added at ", colls[0][0]+1,"|", indiv)
                        #print("Collision info", colls)
                        next_colls = self.map.getIndividualCollisions(indiv)
                        if len(next_colls) > 0:
                            #print("Accepted 1")
                            next_need_fix.add((indiv,next_colls))
                        else:
                            indiv.score = indiv.calcLongitude()
                            start_individuals.append(indiv)
            
                #Calculate new Individual 1
                changed_path = ind.getPath()
                move_vector = -Vector.round(collided_line.u * (self.point_distance), self.map_size_order)
                translated_point = Point(collided_line.p1.x + move_vector.x, collided_line.p1.y + move_vector.y)
                algorithm()
                

                #Calculate new Individual 2
                changed_path = ind.getPath()
                move_vector = Vector.round(collided_line.u * (self.point_distance), self.map_size_order)
                translated_point = Point(collided_line.p2.x + move_vector.x, collided_line.p2.y + move_vector.y)
                algorithm()
                    
                #print("NEXT ITER")
            need_fix = next_need_fix
            #End while    
        print("Start with: ", len(start_individuals))
        return start_individuals

    def selection_func(self) -> list[Individuo]:
        return self.population

    def cross_func(self, selected_pop) -> list[Individuo]:
        return selected_pop

    def mutation_func(self, crossed_pop) -> list[Individuo]:
        return crossed_pop
    
    def replace_func(self, selected, crossed_pop, mutated_pop) -> list[Individuo]:
        return mutated_pop

    def stop_func(self) -> bool:
        return True

    def display_func(self) -> None:
        pass