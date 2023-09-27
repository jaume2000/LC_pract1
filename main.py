from matplotlib.animation import FuncAnimation
from genetic_algorithms.genetic_classes import PrintingGE, RandomGE, ElasticRopeGE
from utils.map import Map
from utils.math_lines import Point, Line
import matplotlib.pyplot as plt
import threading

def startExperiment(ge_map,plot_n_individuals):
#Preparamos la animación

    fig, ax = plt.subplots()
    fittest_line, = ax.plot([ge_map.startPoint.x, ge_map.endPoint.x], [ge_map.startPoint.y, ge_map.endPoint.y], c='green', linewidth=3, zorder=2)
    suboptimal_lines = []
    #Puntos de inicio y final
    plt.scatter([ge_map.startPoint.x, ge_map.endPoint.x], [ge_map.startPoint.y, ge_map.endPoint.y], marker='o', c='green')

    #Dibuja los obstaculos
    for obs in ge_map.obstacles:
        obs_x = [obs.p1.x, obs.p2.x]
        obs_y = [obs.p1.y, obs.p2.y]
        plt.plot(obs_x, obs_y, color='black', linewidth=4)


    #Opciones básicas del gráfico
    plt.xlim(0, ge_map.width)
    plt.ylim(0, ge_map.height)
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Línea de (0,0) a (10,10)')

    def update(frame):
        # Actualiza la gráfica con los datos
        for i in range(1,plot_n_individuals):
            if i < len(myGE.population) and i < plot_n_individuals:
                path = myGE.population[i].getPath()
                if i >= len(suboptimal_lines):
                    #Update line
                    new_line, = ax.plot([p.x for p in path],[p.y for p in path], linewidth=1, zorder=1)
                    suboptimal_lines.append(new_line)
                else:
                    #Create line
                    suboptimal_lines[i-1].set_xdata([p.x for p in path])
                    suboptimal_lines[i-1].set_ydata([p.y for p in path])
        if myGE.fittest != None:
            fittest_path = myGE.fittest.getPath()
            fittest_line.set_ydata(list(map(lambda p: p.y, fittest_path)))
            fittest_line.set_xdata(list(map(lambda p: p.x, fittest_path)))


    ani = FuncAnimation(fig, update, interval=100)



    #Crea
    algorithm_thread = threading.Thread(target=myGE.start)

    algorithm_thread.start()


    # Mostrar el gráfico
    plt.show()

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

cuadratic_line_map = []
gap = 2
for i in range(6):
    x = 10 + 5*i
    barrier_size = 80*(2**-i)
    for j in range(2**i):


        y1 = 10 + j*barrier_size
        y2 = 10 + barrier_size+ j*barrier_size - gap
        l = Line(x, y1, x, y2)
        cuadratic_line_map.append(l)


ge_map = Map(100,100, Point(5,50), Point(95,50), incremental_lines_map )
ge_map = buildMap("./maps/test_map1.txt")

myGE = ElasticRopeGE(100, 200, 10, 5, map=ge_map)
startExperiment(ge_map, plot_n_individuals=20)
