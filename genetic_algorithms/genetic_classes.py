
from abc import abstractmethod
from abc import ABCMeta

from utils.map import Map

class IGeneticAlgorithm(metaclass=ABCMeta):
    @abstractmethod
    def population_generation_func(self, map:Map):
        pass

    @abstractmethod
    def selection_func(self, population):
        pass

    @abstractmethod
    def cross_func(self, population):
        pass

    @abstractmethod
    def mutation_func(self, population):
        pass
    
    @abstractmethod
    def replace_func(self, ):
        pass

    @abstractmethod
    def stop_func(self):
        pass

    @abstractmethod
    def display_func(self):
        pass


class GE1(IGeneticAlgorithm):
    def __init__(self):
        super().__init__()
    
    def population_generation_func(self):
        pass

    def selection_func(self):
        pass

    def cross_func(self):
        pass

    def mutation_func(self):
        pass
    
    def replace_func(self):
        pass

    def stop_func(self):
        pass

    def display_func(self):
        pass
    

print(GE1())