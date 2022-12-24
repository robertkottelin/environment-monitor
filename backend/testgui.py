import PySimpleGUI as sg
import random
import time
import datetime
import os
import glob
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
# import RPi.GPIO as GPIO  # Uncomment this line if using a Raspberry Pi to control the lamp

use_fake_data = True  # Set this to False to use real temperature data
table_content = []  # List to store the temperature data

if not use_fake_data:
    # Initialize the temperature sensor
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

x=1
def oscillating_temp():
  global x  # Declare x as a global variable
  # Generate a temperature value that oscillates between 21 and 23
  osc_temp = 21 + 2 / (1 + math.exp(-x))
  x += 0.1  # Increment x to produce the oscillating effect
  return osc_temp

def generate_temperature_data():
    if use_fake_data:
        global x  # Declare x as a global variable
        # Generate a temperature value that oscillates between 21 and 23
        osc_temp = 21 + 2 / (1 + math.exp(-x))
        x += 0.1  # Increment x to produce the oscillating effect
        return osc_temp
    else:
        # Read the temperature data from the sensor
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
        equals_pos = lines[1].find(b't=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temperature_data_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            table_content.append(temperature_data_c)
            return temperature_data_c

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
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

# GUI
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
    [sg.Canvas(key = '-CANVAS-')]
]

# Create the window
window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
                   auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
                   default_element_size=(30, 10), finalize=True)

# matplotlib
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
    data = generate_temperature_data()
    table_values = window['-TABLE-'].get()
    table_values.insert(0, [len(table_values) + 1, data, timestamp])
    update_figure(data)
    window['-TABLE-'].update(table_values)

window.close()