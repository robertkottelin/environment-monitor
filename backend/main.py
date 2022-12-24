import time
import PySimpleGUI as sg
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from database import config_database, connect, insert_temperature
from read_temp import read_temperature, generate_sigmoid_fake_data

use_fake_data = True  # Set this to False to use real temperature data
table_content = []  # List to store the temperature data

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
    axes[0].plot(x, y, 'r-')
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()


# GUI
layout = [
    [sg.Input(key='-TEMP-')],
    [sg.Button('Set temperature')],
    [sg.Table(
        headings=['Index', 'Celsius', 'Timestamp'],
        values=[[]],
        expand_x=True,
        key='-TABLE-'
    )],
    [sg.Canvas(key='-CANVAS-')]
]

# Create the window
window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
                   auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
                   default_element_size=(30, 10), finalize=True)

# matplotlib
fig = Figure(figsize=(5, 4))
fig.add_subplot(111).plot([], [])
figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
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

    if use_fake_data:
        data = generate_sigmoid_fake_data()
    else:
        data = read_temperature()

    table_values = window['-TABLE-'].get()
    table_values.insert(0, [len(table_values) + 1, data, timestamp])
    update_figure(data)
    window['-TABLE-'].update(table_values)

window.close()
