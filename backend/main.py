import time
import PySimpleGUI as sg
import math
import matplotlib.pyplot as plt
import datetime

# from database import config_database, connect, insert_temperature
from read_temp import read_temperature

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define a global variable to store the value of x
x = 0

def oscillating_temp():
  global x  # Declare x as a global variable
  # Generate a temperature value that oscillates between 21 and 23
  osc_temp = 21 + 2 / (1 + math.exp(-x))
  x += 0.1  # Increment x to produce the oscillating effect
  return osc_temp

temperature_data = []

def update_figure(figdata):
    if not isinstance(figdata, float):
        raise ValueError('figdata must be a float')
    # Add the new temperature data point to the list
    temperature_data.append((datetime.datetime.now(), figdata))
    # Extract the x-axis and y-axis data from the temperature data list
    x = [point[0] for point in temperature_data]
    y = [point[1] for point in temperature_data]
    # Plot the data on the matplotlib figure
    axes = fig.axes
    axes[0].plot(x,y,'r-')
    FigureCanvasTkAgg.draw()
    FigureCanvasTkAgg.get_tk_widget().pack()


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


fig = Figure(figsize = (5,4))
fig.add_subplot(111).plot([],[])
figure_canvas_agg = FigureCanvasTkAgg(fig,window['-CANVAS-'].TKCanvas)
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()


interval = 1  # seconds

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
    table_values.insert(0, [len(table_values) +1, osc_temp, timestamp])
    window['-TABLE-'].update(table_values)

    update_figure(table_values)    
    
    # Insert the temperature into the database
    # insert_temperature(conn, cur, sensor_data)

window.close()