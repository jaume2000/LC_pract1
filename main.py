from matplotlib.animation import FuncAnimation
from genetic_algorithms.genetic_classes import PrintingGE, RandomGE, ElasticRopeGE
from utils.map import Map
from utils.math_lines import Point, Line
import matplotlib.pyplot as plt
import threading

def startExperiment(plot_n_individuals):
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
        plt.plot(obs_x, obs_y, color='black')


    #Opciones básicas del gráfico
    plt.xlim(0, 100)
    plt.ylim(0, 100)
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
                    new_line, = ax.plot([p.x for p in path],[p.y for p in path], c='gray', linewidth=1, zorder=1)
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


#Definir y empezar el experimento

ge_map = Map(100,100, Point(5,50), Point(95,50), [Line(10,20,10,80),Line(20,20,20,80),Line(30,20,30,80),Line(40,20,40,80),Line(50,20,50,80),Line(60,20,60,80),Line(70,20,70,80),Line(80,20,80,80),Line(90,20,90,80)])
myGE = ElasticRopeGE(1000, 200, 1, 5, map=ge_map)
startExperiment(plot_n_individuals=4)

