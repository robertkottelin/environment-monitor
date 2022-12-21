import PySimpleGUI as sg
import random
import time
import psycopg2
import os
import glob
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


def generate_temperature_data():
    """Generates temperature data.

    If use_fake_data is True, generates a random temperature value between 22 and 24 degrees Celsius.
    If use_fake_data is False, reads the temperature data from the sensor.
    """
    if use_fake_data:
        random_temperature_data = random.uniform(22, 24)
        table_content.append(random_temperature_data)
        return random_temperature_data
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


def control_lamp(state: str):
    """Controls a lamp.

    Args:
        state: The state to set the lamp to. Valid values are 'on' and 'off'.
    """
    # Set up the GPIO pin for the relay
    relay_pin = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)

    if state == 'on':
        # Turn the relay on
        GPIO.output(relay_pin, GPIO.HIGH)
    elif state == 'off':
        # Turn the relay off
        GPIO.output(relay_pin, GPIO.LOW)
    else:
        raise ValueError(f'Invalid state: {state}')


def create_cursor():
    """Connects to the database and creates a cursor."""
    conn = psycopg2.connect(
        host="localhost",
        database="mydatabase",
        user="user",
        password="password"
    )
    cursor = conn.cursor()
    return conn, cursor


def insert_temp(temperature_data_c, temp_f, cursor):
    """Inserts a row into the temperature table"""
    query = "INSERT INTO temperature (temp_c, temp_f) VALUES (%s, %s)"
    cursor.execute(query, (temperature_data_c, temp_f))


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
