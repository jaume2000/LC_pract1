from genetic_algorithms.genetic_classes import IGeneticAlgorithm

class GeneticAlgorithm:
    def __init__(
            self,
            mapa,
            ge:IGeneticAlgorithm
    ):
        self.mapa = mapa
        self.ge = ge
        self.population = []
        self.fittest = None
    
    def init(self):
        t = 0
        fin = False
        self.population_generation_func(self.mapa)
        while not fin:
            selected = self.ge.selection_func()
            crossed = self.ge.cross_func(selected)
            mutated = self.ge.mutation_func(crossed)
            self.population = self.ge.replace_func(selected, crossed, mutated)
            fin = self.stop_func(t)
            self.display_func(self.population)
            t+=1
        