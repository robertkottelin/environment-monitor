import PySimpleGUI as sg
import random
import time

# Generate random data between 20.0 and 24.0
def generate_random_temperature_data():
    return random.uniform(20.0, 24.0)

# Set the temperature data to a specific value
def set_temperature_data(temp_value):
    global random_data
    random_data = temp_value

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
]

# Create the window
window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
                   auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
                   default_element_size=(30, 10), finalize=True)

# Set an interval for generating and updating data
interval = 1  # seconds

# Initialize the random_data variable as a global variable
random_data = generate_random_temperature_data()

# Run the event loop indefinitely
while True:
    # Check for events
    event, values = window.read(timeout=interval*1000)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Set temperature':
        # Update the temperature data with the input value
        temp_value = values['-TEMP-']
        set_temperature_data(temp_value)
    
    # Generate and update the data every interval seconds
    timestamp = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
    table_values = window['-TABLE-'].get()
    table_values.insert(0, [len(table_values) + 1, random_data, timestamp])
    window['-TABLE-'].update(table_values)

window.close()