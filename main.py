from matplotlib.animation import FuncAnimation
from genetic_algorithms.genetic_classes import PrintingGE, RandomGE, ElasticRopeGE, NoneGE
from utils.map import Map
from utils.math_lines import Point, Line
import matplotlib.pyplot as plt
import threading

def startExperiment(ge,ge_map,plot_n_individuals):
#Preparamos la animación
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,5))
    ax1.set_aspect('equal')

    ax2.set_xlabel('Generación')
    ax2.set_ylabel('Fitness')
    ax2.set_title('Fitness del mejor individuo')
    fittest_results, = ax2.plot([0,1],[0,0])

    fittest_line, = ax1.plot([ge_map.startPoint.x, ge_map.endPoint.x], [ge_map.startPoint.y, ge_map.endPoint.y], c='green', linewidth=3, zorder=2)
    suboptimal_lines = []
    #Puntos de inicio y final
    ax1.scatter([ge_map.startPoint.x, ge_map.endPoint.x], [ge_map.startPoint.y, ge_map.endPoint.y], marker='o', c='green')

    #Dibuja los obstaculos
    for obs in ge_map.obstacles:
        obs_x = [obs.p1.x, obs.p2.x]
        obs_y = [obs.p1.y, obs.p2.y]
        ax1.plot(obs_x, obs_y, color='black', linewidth=4)


    #Opciones básicas del gráfico
    ax1.set_xlim(0, ge_map.width)
    ax1.set_ylim(0, ge_map.height)
    ax1.set_title('Evolución en el mapa')

    def update(frame):
        # Actualiza la gráfica con los datos
        for i in range(1,plot_n_individuals):
            if i < len(ge.population) and i < plot_n_individuals:
                path = ge.population[i].getPath()
                if i >= len(suboptimal_lines):
                    #Update line
                    new_line, = ax1.plot([p.x for p in path],[p.y for p in path], linewidth=1, zorder=1)
                    suboptimal_lines.append(new_line)
                else:
                    #Create line
                    suboptimal_lines[i-1].set_xdata([p.x for p in path])
                    suboptimal_lines[i-1].set_ydata([p.y for p in path])
        if ge.fittest != None:
            fittest_path = ge.fittest.getPath()
            fittest_line.set_ydata(list(map(lambda p: p.y, fittest_path)))
            fittest_line.set_xdata(list(map(lambda p: p.x, fittest_path)))

        fittest_results_y = myGE.results.copy()
        fittest_results_x = list(range(0,len(fittest_results_y)))
        fittest_results.set_data(fittest_results_x,fittest_results_y)
        ax2.set_xlim(0, ge_map.width)
        max_y = 1000 if len(fittest_results_y)==0 else fittest_results_y[0]+100
        min_y = 900 if len(fittest_results_y)==0 else fittest_results_y[-1]-100
        ax2.set_ylim(min_y, max_y)
        ax2.set_xlim(0, max(50,len(fittest_results_x)+5))


    ani = FuncAnimation(fig, update, interval=100)



    #Crear un thread para ejecutar el algoritmo y que animación y algoritmo vayan en paralelo
    algorithm_thread = threading.Thread(target=ge.start)

    algorithm_thread.start()


    # Mostrar el gráfico
    plt.show()

#---------------------- END OF START EXPERIMENT ----------------------------------------

def buildMap(file):
    with open(file) as f:
        width, height = [int(i) for i in f.readline().split()]
        start_x, start_y = [int(i) for i in f.readline().split()]
        end_x, end_y = [int(i) for i in f.readline().split()]
        lines = []
        
        l = [int(i) for i in f.readline().split()]

        while l:
            x1,y1,x2,y2 = l
            lines.append(Line(x1,y1,x2,y2))
            l = [int(i) for i in f.readline().split()]

    return Map(width, height, Point(start_x, start_y), Point(end_x, end_y), lines)
        
#Definir y empezar el experimento

incremental_lines_map = [Line(10+5*i,50 - 1.3**(i),10+5*i,50 + 1.3**(i)) for i in range(15)]

one_path_map = [Line(10+5*i, 20 - (20 * (i % 2)) -2,10+5*i,80 + (20 * ((i+1) % 2)) +2) for i in range(17)]

ge_map = Map(100,100, Point(5,50), Point(95,50), incremental_lines_map )
ge_map = buildMap("./maps/test_map1.txt")

#ge_map = Map(100,100, Point(5,50), Point(95,50), [Line(50,20,50,80)])

#myGE = NoneGE(ge_map)

myGE = ElasticRopeGE(
    start_population_size=  50,
    stop_gen=               1000,
    converge_gens=          50,
    cross_prob=             0.5,
    cross_method=2,
    mutation_prob=          0.5,
    mutation_traslation_radius=300,
    max_mutations_per_ind=  5,
    mutation_method=2,
    map_size_order=5,
    point_distance=         1,
    map=ge_map)

startExperiment(myGE,ge_map, plot_n_individuals=50)
