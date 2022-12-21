import PySimpleGUI as sg
import random
import time
import psycopg2
import os
import glob

use_fake_data = True
table_content = []

if not use_fake_data:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

# Read the temperature data from the sensor or generate fake data

# Generate data

def generate_temperature_data():
    if use_fake_data:
        random_temperature_data = random.uniform(22, 24)
        table_content.append(random_temperature_data)
        return random_temperature_data
    else:
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

# Connect to the database and create a cursor
def create_cursor():
    conn = psycopg2.connect(
        host="localhost",
        database="mydatabase",
        user="user",
        password="password"
    )
    cursor = conn.cursor()
    return conn, cursor

# Insert a row into the temperature table


def insert_temp(temp_c, temp_f, cursor):
    query = "INSERT INTO temperature (temp_c, temp_f) VALUES (%s, %s)"
    cursor.execute(query, (temp_c, temp_f))


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
]

# Create the window
window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
                   auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
                   default_element_size=(30, 10), finalize=True)

# Set an interval for generating and updating data
interval = 1  # seconds


# Run the event loop indefinitely
while True:
    # Check for events
    event, values = window.read(timeout=interval*1000)
    if event == sg.WIN_CLOSED:
        break
    # elif event == 'Set temperature':
    #     # Update the temperature data with the input value
    #     temp_value = values['-TEMP-']
    #     set_temperature_data(temp_value)

    # Generate and update the data every interval seconds
    timestamp = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
    data = generate_temperature_data()
    table_values = window['-TABLE-'].get()
    table_values.insert(0, [len(table_values) + 1, data, timestamp])
    window['-TABLE-'].update(table_values)

window.close()
