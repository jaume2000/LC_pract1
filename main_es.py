from enfriamiento_simulado.enfriamiento_simulado import TraslatingPoints
from utils.map import buildMap
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading


def startExperiment(es_alg:TraslatingPoints):

    es_alg_map = es_alg.map

    #Preparamos la animación
    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,5))
    ax1.set_aspect('equal')

    ax2.set_xlabel('Generación')
    ax2.set_ylabel('Fitness')
    ax2.set_title('Fitness del mejor individuo')
    fittest_results, = ax2.plot([0,1],[0,0])

    fittest_line, = ax1.plot([es_alg_map.startPoint.x, es_alg_map.endPoint.x], [es_alg_map.startPoint.y, es_alg_map.endPoint.y], c='green', linewidth=3, zorder=2)
    suboptimal_lines = []
    #Puntos de inicio y final
    ax1.scatter([es_alg_map.startPoint.x, es_alg_map.endPoint.x], [es_alg_map.startPoint.y, es_alg_map.endPoint.y], marker='o', c='green')

    #Dibuja los obstaculos
    for obs in es_alg_map.obstacles:
        obs_x = [obs.p1.x, obs.p2.x]
        obs_y = [obs.p1.y, obs.p2.y]
        ax1.plot(obs_x, obs_y, color='black', linewidth=4)


    #Opciones básicas del gráfico
    ax1.set_xlim(0, es_alg_map.width)
    ax1.set_ylim(0, es_alg_map.height)
    ax1.set_title('Evolución en el mapa')

    def update(frame):
        if es_alg.fittest != None:
            fittest_path = es_alg.fittest.getPath()
            fittest_line.set_ydata(list(map(lambda p: p.y, fittest_path)))
            fittest_line.set_xdata(list(map(lambda p: p.x, fittest_path)))

        fittest_results_y = es_alg.results.copy()
        fittest_results_x = list(range(0,len(fittest_results_y)))
        fittest_results.set_data(fittest_results_x,fittest_results_y)
        ax2.set_xlim(0, es_alg_map.width)
        max_y = 1000 if len(fittest_results_y)==0 else fittest_results_y[0]+100
        min_y = 900 if len(fittest_results_y)==0 else fittest_results_y[-1]-100
        ax2.set_ylim(min_y, max_y)
        ax2.set_xlim(0, max(50,len(fittest_results_x)+5))


    ani = FuncAnimation(fig, update, interval=100)



    #Crear un thread para ejecutar el algoritmo y que animación y algoritmo vayan en paralelo
    algorithm_thread = threading.Thread(target=es_alg.start)

    algorithm_thread.start()


    # Mostrar el gráfico
    plt.show()

#---------------------- END OF START EXPERIMENT ----------------------------------------
        

ef_map = buildMap("./maps/test_map1.txt")

myEF = TraslatingPoints(
    neighbour_size=         50,
    temp_decrement=         0.95,
    stop_t_dec_gen=         20,
    stop_gen=               150,
    converge_gens=          50,
    stop_temperature=       0.0001,
    traslation_radius=      300,
    max_mutations_per_ind=  5,
    point_distance=         1,
    map_size_order=1,
    map=ef_map)

#startExperiment(myGE,es_alg_map, plot_n_individuals=50)

startExperiment(myEF)

