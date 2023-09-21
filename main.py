from matplotlib.animation import FuncAnimation
from genetic_algorithms.genetic_classes import PrintingGE, RandomGE
from utils.map import Map
from utils.math_lines import Point, Line
import matplotlib.pyplot as plt
import threading

ge_map = Map(100,100, Point(10,10), Point(90,90), [Line(30,0, 30, 70), Line(30,70, 50,80), Line(50,20, 70,30) ,Line(70,100, 70,30)])
myGE = RandomGE(1000, 7, 200, 50, map=ge_map)


#Preparamos la animación

fig, ax = plt.subplots()
line, = ax.plot([ge_map.startPoint.x, ge_map.endPoint.x], [ge_map.startPoint.y, ge_map.endPoint.y], c='green')

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
plt.legend()

def update(frame):
    # Actualiza la gráfica con los datos
    fittest_path = myGE.fittest.getPath()
    line.set_ydata(list(map(lambda p: p.y, fittest_path)))
    line.set_xdata(list(map(lambda p: p.x, fittest_path)))
ani = FuncAnimation(fig, update, interval=100)



#Crea
algorithm_thread = threading.Thread(target=myGE.start)

algorithm_thread.start()


# Mostrar el gráfico
plt.show()





