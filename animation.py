#%%

import numpy as np
import pandas as pd
from numpy import genfromtxt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import matplotlib.collections as mcoll


fig, ax = plt.subplots()
cmap = mcolors.ListedColormap(["white", "black", "red",])
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

def animate(xCorr, yCorr):
    data = genfromtxt("map.csv", delimiter=";")
    data[xCorr, yCorr] = 2
    im.set_data(data)
    # return a list of the artists that need to be redrawn
    return [im, grid]

anim = animation.FuncAnimation(fig, animate(2,2), frames=2, interval=1, blit=True, repeat=True)
plt.show()


# %%
# %%
