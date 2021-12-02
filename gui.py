
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors
from numpy import genfromtxt
import matplotlib.collections as mcoll
import matplotlib.animation as animation
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from math import atan2, sqrt, pow, cos, sinh, radians
import math
import time




#global variables
i= 0 
goal_x = 0
goal_x = 0
robot_pos_x = 0
robot_pos_y = 0
steer_angle = 0
robot_degree_angle = 0
theta = 0
robot_trajectory = [[robot_pos_x,robot_pos_x]]
distance_tolerance = 0.2
angular_tolerance = 0.02

ROBOT_BASELINE = 0.1

map_space = genfromtxt("nmvr/nmvr/map.csv", delimiter=";")

matplotlib.use("TkAgg")

#setting GUI colors
fig, ax = plt.subplots()
cmap = mcolors.ListedColormap(["gray", "black", "lime", "green", "blue"])
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

#reading map data
map_space = genfromtxt("nmvr/nmvr/map.csv", delimiter=";")
im = ax.imshow(map_space, cmap=cmap, norm=norm)
data = map_space

#setting up grid on a plot view
grid = np.arange(-0.5, 51, 1)
xmin, xmax, ymin, ymax = -0.5, 50.5, -0.5, 50.5
lines = ([[(x, y) for y in (ymin, ymax)] for x in grid]
         + [[(x, y) for x in (xmin, xmax)] for y in grid])
grid = mcoll.LineCollection(lines, linestyles="solid", linewidths=0.3, color="white")
ax.add_collection(grid)

def draw_figure(canvas, figure):
    
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

def animation_frame(i):
    #data showed on a plot, static map currently
    #data = np.random.rand(10,10)*2 - 0.5 #animation working test
    im.set_data(data)
    return[im, grid]

def euclidian_distance():
    return sqrt(pow((goal_x - robot_pos_x), 2) + pow((goal_y - robot_pos_y), 2))


def linear_vel(p_const = 2):
    return p_const + euclidian_distance(robot_pos_x, robot_pos_y, goal_x, goal_y)
    
def steering_angle(robot_pos_x, robot_pos_y, goal_y, goal_x):
    s_a =  atan2(goal_x - robot_pos_x, goal_y - robot_pos_y)
    return s_a


def angluar_vel(p_const = 2):
    return p_const + (steering_angle - theta)

def move():
    new_x = (robot_pos_x + ROBOT_BASELINE/2) * cos(theta)
    new_y = (robot_pos_y + ROBOT_BASELINE/2) * sinh(theta)
    next_pos = [new_x, new_y]
    robot_trajectory.apped(next_pos)

def calc_theta():
    return ((robot_trajectory[-1][0] - robot_trajectory[-2][0]) - 
    (robot_trajectory[-1][1] - robot_trajectory[-2][1])) / ROBOT_BASELINE

def move2goal(robot_pos_x, robot_pos_y, goal_x, goal_y):
    while(robot_pos_x != goal_x) and (robot_pos_y != goal_x):

        direction = angle_calc(robot_pos_x, robot_pos_y, goal_y, goal_x)
        data[robot_pos_x, robot_pos_y] = 3
        
        if direction == 90:
            robot_pos_y = robot_pos_y - 1
        elif direction == 135:
            robot_pos_y = robot_pos_y - 1
            robot_pos_x = robot_pos_x - 1
        elif direction == 180:
            robot_pos_x = robot_pos_x -1
        elif direction == 225:
            robot_pos_y = robot_pos_y + 1
            robot_pos_x = robot_pos_x -1
        elif direction == 270:
            robot_pos_y = robot_pos_y +1
        elif direction == 315:
            robot_pos_y = robot_pos_y + 1
            robot_pos_x = robot_pos_x +1
        elif direction == 0:
            robot_pos_x = robot_pos_x +1
        elif direction == 45:
            robot_pos_x = robot_pos_x + 1
            robot_pos_y = robot_pos_y -1
        
        
        data[robot_pos_x, robot_pos_y] = 2
        
        


def angle_calc(robot_pos_x, robot_pos_y, goal_y, goal_x):
    s_a = math.degrees(steering_angle(robot_pos_x, robot_pos_y, goal_y, goal_x))
    print("Robot angle: " + str((s_a)))
    
    if s_a<= 27.5 or s_a >337.5:
        m_a = 0
    elif 67.5 <= s_a > 27.5:
        m_a = 45
    elif 112.5 <= s_a > 67.5:
        m_a = 90
    elif 157.5 <= s_a >112.5:
        m_a = 135
    elif 202.5 <= s_a > 157.5:
        m_a = 180
    elif 247.5 <= s_a > 202.5:
        m_a = 225
    elif 292.5 <= s_a > 247.5:
        m_a = 270
    else:
        m_a = 315
    print("Moving angle is: " + str(m_a))
    return m_a



#setting up layout for app gui
layout= [[sg.Text("Basic simulator GUI")],
        [sg.Canvas(key="-CANVAS-")],

        [
        sg.InputText(size = (2,1), key= "-SPAWN_POS_X-"), sg.InputText(size = (2,1), key= "-SPAWN_POS_Y-"),
        sg.Button("Spawn"),
        sg.Button("Set Goal"),
        sg.InputText(size = (2,1), key= "-GOAL_POS_X-"), sg.InputText(size = (2,1), key= "-GOAL_POS_Y-")
        ],

        #text outputs eg. robot pos and degree
        [
        sg.Text(robot_pos_x, key = "-ROBOT_POS_X-"),
        sg.Text(robot_pos_y, key = "-ROBOT_POS_Y-"),
        sg.Text((str(steer_angle) +  "°"), key = "-DEGREE_ANGLE-")
        ],

        #close button pos
        [sg.Button("Go to"),sg.Button("Close")]]

#setting window object
window = sg.Window("Sim GUI", layout, finalize=True, element_justification="center")
fig_canvas_agg = draw_figure(window["-CANVAS-"].TKCanvas, fig)

#animation of matplotlib plot
anim = animation.FuncAnimation(fig, animation_frame, frames = 2, interval = 0,
                                blit= True, repeat = True)

while True:

    #reading events and values from window
    event, values = window.read()

    if event in(sg.WIN_CLOSED, "Cancel"):
        #kill window
        break
    
    #spawn button press
    if event == "Spawn":
        robokot_spawn_pos_x = values["-SPAWN_POS_X-"]
        robokot_spawn_pos_y = values["-SPAWN_POS_Y-"]
        print(robokot_spawn_pos_x, robokot_spawn_pos_y)
        robot_pos_y = int(robokot_spawn_pos_x)
        robot_pos_x = int(robokot_spawn_pos_y)
        data[robot_pos_x, robot_pos_y] = 2
        
    #goal button press
    if event == "Set Goal":
        goal_y = int(values["-GOAL_POS_X-"])
        goal_x = int(values["-GOAL_POS_Y-"])
        print(goal_x, goal_y)
        data[goal_x, goal_y] = 4

    #close button press
    if event == "Close":
        #kill window
        break

    if event == "Go to":
        move2goal(robot_pos_x, robot_pos_y, goal_x, goal_y)
    
    #updating position and degree on a window
    window["-ROBOT_POS_X-"].update(robot_pos_x)
    window["-ROBOT_POS_Y-"].update(robot_pos_x)
    window["-DEGREE_ANGLE-"].update(steer_angle)

window.close