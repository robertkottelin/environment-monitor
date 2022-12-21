
import os
import glob
import time
import PySimpleGUI as sg
import random
import psycopg2

# Find the path of the DS18B20 temperature sensor
# Alternatively, use the fake data generator
use_fake_data = True

table_content = []

if not use_fake_data:
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

# Read the temperature data from the sensor or generate fake data
def read_temp_raw():
    if use_fake_data:
        return [b'', b't=23000\n']
    else:
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find(b't=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        table_content.append(temp_c)
        return temp_c, temp_f

# Generate fake temperature data
def generate_fake_temp():
    temp_c = random.uniform(20, 30)
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    table_content.append(temp_c)
    return temp_c, temp_f

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



# Create a graphical user interface with PySimpleGUI
sg.theme('DarkAmber')

layout = [
	[sg.Table(
		headings = ['Observation','Result'], 
		values = table_content, 
		expand_x = True, 
		hide_vertical_scroll = True,
		key = '-TABLE-')],
	[sg.Input(key = '-INPUT-',expand_x = True),sg.Button('Get')],
	[sg.Canvas(key = '-CANVAS-')]
]

window = sg.Window('Temperature Monitor', layout)

# conn, cursor = create_cursor()

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if use_fake_data:
        temp_c, temp = generate_fake_temp()
    else:
        temp

