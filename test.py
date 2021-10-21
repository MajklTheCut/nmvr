import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



#Function for drawing
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#Layout creation
layout = [[sg.Text('Embed Matplotlib Plot')],
          [sg.Canvas(key='-CANVAS-')],
          [sg.Button("Add"), sg.Button("Clear")]]

#Create a window. finalize=Must be True.
window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True, element_justification='center', font='Monospace 18')

#Create a fig for embedding.
fig = plt.figure(figsize=(5, 4))
ax = fig.add_subplot(111)
ax.set_ylim(-10, 10)

#Associate fig with Canvas.
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

#Event loop
while True:
    event, values = window.read()
    print(event, values)
    # sg.Print(event, values)
    
    if event in (None, "Cancel"):
        break
    
    elif event == "Add":
        #Creating appropriate plot data
        t = np.linspace(0, 7, 100)
        afreq = np.random.randint(1, 10)
        amp = np.random.randint(1, 10)
        y = amp * np.sin(afreq * t)
        
        #plot
        ax.plot(t, y, alpha=0.4)
        
        #After making changes, fig_agg.draw()Reflect the change with.
        fig_agg.draw()

    elif event == "Clear":
        ax.cla()
        fig_agg.draw()

#close the window.
window.close()