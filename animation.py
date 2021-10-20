import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib
from numpy import genfromtxt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import matplotlib.collections as mcoll

window = tk.Tk()
window.title("Sim GUI")
operator= ""

canvas = tk.Canvas(window, height= 600, width=600, bg="White")
canvas.pack()

frame = tk.Frame(window, bg="Light Blue")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)


fig, ax = plt.subplots()
cmap = mcolors.ListedColormap(["white", "black", "lime",])
bounds = [-0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

map_space = genfromtxt("map.csv", delimiter=";")
im = ax.imshow(map_space, cmap=cmap, norm=norm)

grid = np.arange(-0.5, 51, 1)
xmin, xmax, ymin, ymax = -0.5, 50.5, -0.5, 50.5
lines = ([[(x, y) for y in (ymin, ymax)] for x in grid]
         + [[(x, y) for x in (xmin, xmax)] for y in grid])
grid = mcoll.LineCollection(lines, linestyles="solid", linewidths=0.3, color="gray")
ax.add_collection(grid)

def animate(i):
    data = genfromtxt("map.csv", delimiter=";")
    data[5,5] = 2
    im.set_data(data)
    # return a list of the artists that need to be redrawn
    return [im, grid]


anim = animation.FuncAnimation(fig, animate, frames=2, interval=1, blit=True, repeat=True)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=1)

tk.mainloop()
