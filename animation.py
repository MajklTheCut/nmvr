
import matplotlib
import numpy as np
import pandas as pd
from numpy import genfromtxt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import matplotlib.collections as mcoll
import PySimpleGUI as sg

matplotlib.use("TkAgg")


fig, ax = plt.subplots()
cmap = mcolors.ListedColormap(["gray", "black", "lime",])
bounds = [-0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

map_space = genfromtxt("/home/nvmr/Documents/nmvr/nmvr/map.csv", delimiter=";")
im = ax.imshow(map_space, cmap=cmap, norm=norm)

def moveRobot(xCoor, yCoor):
    map_space[xCoor,yCoor] = 2

moveRobot(2,2)

grid = np.arange(-0.5, 51, 1)
xmin, xmax, ymin, ymax = -0.5, 50.5, -0.5, 50.5
lines = ([[(x, y) for y in (ymin, ymax)] for x in grid]
         + [[(x, y) for x in (xmin, xmax)] for y in grid])
grid = mcoll.LineCollection(lines, linestyles="solid", linewidths=0.3, color="white")
ax.add_collection(grid)


def animate(i):
    data = genfromtxt("/home/nvmr/Documents/nmvr/nmvr/map.csv", delimiter=";")
    data[5,5] = 2
    im.set_data(data)
    return [im, grid]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

layout= [[sg.Text("Basic simulator GUI")],
        [sg.Canvas(key="-CANVAS-")],
        [sg.Button("OK")]]

window = sg.Window("Sim GUI", layout, finalize=True, element_justification="center")

fig_canvas_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)

event, values = window.read()

anim = animation.FuncAnimation(fig, animate, frames=2, interval=1, blit=True, repeat=True)

window.close


