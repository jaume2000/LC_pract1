import sys
sys.path.append('../')

from abc import abstractmethod
from abc import ABCMeta
from utils.indiviuo import Individuo
from utils.math_lines import Point
from utils.map import Map
import random
from utils.elastic_ropes import calculate_factibles

class ISimulatedCooling(metaclass=ABCMeta):

    def __init__(
            self,
            map:Map,
            start_temp:float
    ):
        self.map = map
        self.actual = None
        self.fittest = None
        self.gen = 0
        self.fin = False
        self.t = start_temp

        self.results = []

    def start(self)->list[float]:
        self.fin = False
        self.fittest = self.actual = self.generate_first()
        self.results = [self.fittest.score]
        self.display_func()
        while not self.fin:
            neighbors = self.generate_neighbours()
            sel_neighbour = self.select_neighbour(neighbors)
            # Minimizar el coste
            if sel_neighbour.score < self.actual.score:
                self.actual = sel_neighbour
                if self.actual.score < self.fittest.score:
                    self.fittest = self.actual
                    self.fittest_generations_alive = 0
            else:
                if random.random() < self.calc_sel_prob(sel_neighbour):
                    self.actual = sel_neighbour

            self.results.append(self.fittest.score)
            self.decrease_temp()
            self.fin = self.stop_func()
            self.display_func()

            self.gen+=1
            self.fittest_generations_alive+=1

        return self.results
        

    @abstractmethod
    def generate_first(self) -> Individuo:
        #self.map
        #IMPORTANT TO SET the indiviaul.score!
        pass

    @abstractmethod
    def generate_neighbours(self) -> list[Individuo]:
        pass

    @abstractmethod
    def select_neighbour(self, neighbours:list[Individuo]) -> Individuo:
        pass
    
    @abstractmethod
    def calc_sel_prob(self, sel_neighbour):
        pass
    
    @abstractmethod
    def decrease_temp(self):
        pass

    @abstractmethod
    def stop_func(self) -> bool:
        pass

    @abstractmethod
    def display_func(self) -> None:
        #Console display at the end of the cycle.
        pass



class TraslatingPoints(ISimulatedCooling):

    def __init__(self, neighbour_size, temp_decrement, stop_t_dec_gen,stop_gen,
                 converge_gens, stop_temperature, traslation_radius,
                 max_mutations_per_ind, point_distance, map_size_order, map):
        
        super().__init__(map, 1)
        self.neighbour_size = neighbour_size
        self.temp_decrement = temp_decrement
        self.stop_t_dec_gen = stop_t_dec_gen
        self.stop_gen = stop_gen
        self.point_distance = point_distance
        self.map_size_order = map_size_order
        self.converge_gens = converge_gens
        self.traslation_radius = traslation_radius
        self.max_mutations_per_ind = max_mutations_per_ind
        self.stop_temperature = stop_temperature

        self.fittest_generations_alive = 0

    def order_individuals(self, inidivuals:list[Individuo]):
        inidivuals.sort(key=lambda i:i.score)

    def generate_first(self) -> Individuo:
        #self.map
        #IMPORTANT TO SET the indiviaul.score!!!!

        fixing_start_individuals = [] 
        start_individuals =[] 
        first_individual = Individuo([self.map.startPoint,self.map.endPoint], 0)
        first_indiv_cols = self.map.getIndividualCollisions(first_individual)

        fixing_start_individuals.append((first_individual, first_indiv_cols))

        for _ in range(10):
            
            path = [self.map.startPoint] 

            for _ in range(random.randint(1,len(self.map.obstacles))):
                x = round(random.random()*self.map.width, self.map_size_order)
                y = round(random.random()*self.map.height, self.map_size_order)
                new_point = Point(x, y)
                if new_point not in path:
                    path.append(new_point)
            
            path.append(self.map.endPoint)

            indiv = Individuo(path,0) 
            cols = self.map.getIndividualCollisions(indiv)
            if(len(cols)>0):
                fixing_start_individuals.append((indiv,cols))
            else:
                start_individuals.append(indiv)
        start_individuals.extend(calculate_factibles(self.map, self.gen, self.point_distance, self.map_size_order, fixing_start_individuals, self.neighbour_size))

        self.order_individuals(start_individuals)
        self.worst = start_individuals[-1]

        return start_individuals[0]

    def generate_neighbours(self) -> list[Individuo]:
        neighbours = []

        for _ in range(self.neighbour_size):
            n_translations = int(random.random()*(self.max_mutations_per_ind) +1)
            path = self.actual.getPath()
            for _ in range(n_translations):
                
                point_index = random.randint(1, len(path)-2)
                point = path[point_index]

                new_x = round(min(max((random.random()*2-1)*self.traslation_radius*self.t + point.x, 1), self.map.width-1), self.map_size_order)
                new_y = round(min(max((random.random()*2-1)*self.traslation_radius*self.t + point.y, 1), self.map.height-1), self.map_size_order)
                new_point = Point(new_x, new_y)
                if new_point not in path:
                    path[point_index] = new_point
            
            neigh = Individuo(path, self.gen)
            #Si no es factible, lo reparamos
            neigh_colls = self.map.getIndividualCollisions(neigh)
            if len(neigh_colls) > 0:
                fixes = calculate_factibles(self.map, self.gen, self.point_distance, self.map_size_order, [(neigh,neigh_colls)],1)
                if len(fixes) > 0:
                    #print("Mutated!")
                    neighbours.append(fixes[0])
                    neigh = fixes[0]
                    neigh.score = neigh.calcLongitude()
                    neighbours.append(neigh)
            else:
                neigh.score = neigh.calcLongitude()
                neighbours.append(neigh)
        self.order_individuals(neighbours)
        if len(neighbours) >0 and self.worst.score > neighbours[-1].score:
            self.worst = neighbours[-1]
        return neighbours

    #The neighbours can be better or worse than the individual.
    def select_neighbour(self, neighbours:list[Individuo]) -> Individuo:
        #Select the best neighbour
        
        return neighbours[0]

    #sel_neighbour is worst than actual
    def calc_sel_prob(self, sel_neighbour):
        diff = self.fittest.score - self.worst.score
        if diff == 0:
            return 0
        
        return (sel_neighbour.score - self.worst.score) / diff
        

    def decrease_temp(self):
        if self.fittest_generations_alive < self.stop_t_dec_gen:
            self.t = self.t * self.temp_decrement

    def stop_func(self) -> bool:
        return self.gen > self.stop_gen or self.fittest_generations_alive > self.converge_gens or self.t < self.stop_temperature

    def display_func(self) -> None:
        #Console display at the end of the cycle.
        if self.fin:
            print("FIN")
        else:
            print(f"Gen {self.gen:<6} Fittest Score: {self.fittest.score:.5f} . Converge cond: {self.fittest_generations_alive}/{self.converge_gens} Temperature: {self.t:.6f}/{self.stop_temperature}")
        


