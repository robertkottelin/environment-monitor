''' 
# Author: Robert Kottelin 2022-11-22
# Github: https://github.com/robertkottelin/environment-monitor

Script reads temperature data from DS18B20 sensors and sends data to postgresql database 

'''


import os
import glob
import time
import PySimpleGUI as sg
import math
import matplotlib.pyplot as plt

from database import config_database, connect, insert_temperature
from read_temp import read_temperature

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# Define a global variable to store the value of x
x = 0

def oscillating_temp():
  global x  # Declare x as a global variable
  # Generate a temperature value that oscillates between 21 and 23
  temp = 21 + 2 / (1 + math.exp(-x))
  x += 0.1  # Increment x to produce the oscillating effect
  return temp

def main():
    # Set up the layout
    layout = [
        [sg.Input(key='-TEMP-')],
        [sg.Button('Set temperature')],
        [sg.Table(
            headings=['Index', 'Celsius', 'Timestamp'],
            values=[[]],
            expand_x=True,
            key='-TABLE-'
        )],
        # Add a Figure canvas to the layout
        [sg.Canvas(key='-CANVAS-')]
    ]

    # Create the window
    window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
                    auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
                    default_element_size=(30, 10), finalize=True)

    # Add a matplotlib Figure canvas to the window
    figure = plt.Figure()
    plot = figure.add_subplot(111)
    canvas = FigureCanvasTkAgg(figure, master=window['-CANVAS-'].TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
    interval = 2  # seconds
    
    # Run the event loop indefinitely
    while True:
        # Check for events
        event, values = window.read(timeout=interval*1000)
        if event == sg.WIN_CLOSED:
            break

        # Generate and update the data every interval seconds
        timestamp = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
        osc_temp = oscillating_temp()
        table_values = window['-TABLE-'].get()
        table_values.insert(0, [len(table_values) + 1, osc_temp, timestamp])
        window['-TABLE-'].update(table_values)
        
        y_values = [row[1] for row in table_values]
        x_values = [len(table_values)]
        plot.clear()
        plot.plot(x_values, y_values, color='red', linewidth=20)
        canvas.draw()
        
        # Insert the temperature into the database
        # insert_temperature(conn, cur, sensor_data)
    
    window.close()

if __name__ == '__main__':
    main()