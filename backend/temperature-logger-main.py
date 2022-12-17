# # Author: Robert Kottelin 2022-11-22
# # Github: https://github.com/robertkottelin/environment-monitor
# # Python version: 3.10.8 64-bit

# # Script reads temperature data from DS18B20 sensors and sends 
# # data to postgresql database 

# # Standard imports
# import os
# import glob
# import time
# import sqlite3

# import psycopg2

# from configparser import ConfigParser


# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# # Temperature sensors' directory
# base_dir = '/sys/bus/w1/devices/'
# device_folder = glob.glob(base_dir + '28*')[0]
# device_file = device_folder + '/w1_slave'

# # Reads raw data from sensor
# def read_temp_raw():
#     f = open(device_file, 'r')
#     lines = f.readlines()
#     f.close()
#     return lines

# # Reads temperature from raw data and converts it to Celsius (temp_c)
# def read_temp():
#     tempid = 1
#     lines = read_temp_raw()
#     while lines[0].strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = read_temp_raw()
#     equals_pos = lines[1].find('t=')
#     if equals_pos != -1:
#         temp_string = lines[1][equals_pos+2:]
#         temp_c = float(temp_string) / 1000.0
#         # temp_f = temp_c * 9.0 / 5.0 + 32.0
#         tempid += 1
#         return temp_c, tempid
  
# def config(filename='/home/piro/PROJECTS/environment-monitor/backend/database.ini', section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)
#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))
#     return db
  
# def connect():
#     """ Connect to the PostgreSQL database server """
#     conn = None
#     try:
#         # read connection parameters
#         params = config()
  
#         # connect to the PostgreSQL server
#         print('Connecting to the PostgreSQL database...')
#         conn = psycopg2.connect(**params)
          
#         # create a cursor
#         cur = conn.cursor()
          
#     # execute a statement
#         print('PostgreSQL database version:')
#         cur.execute('SELECT version()')
  
#         # display the PostgreSQL database server version
#         db_version = cur.fetchone()
#         #print(db_version)
#         print('Connection successful!')
        
#         lines = read_temp_raw()
#         while lines[0].strip()[-3:] != 'YES':
#             time.sleep(0.2)
#             lines = read_temp_raw()
#         equals_pos = lines[1].find('t=')
#         if equals_pos != -1:
#             temp_string = lines[1][equals_pos+2:]
#             temp_c = float(temp_string) / 1000.0
#             # temp_f = temp_c * 9.0 / 5.0 + 32.0
        
#         postgres_insert_query = """ INSERT INTO temperatures (celsius) VALUES (%s)"""
#         record_to_insert = ([temp_c])
#         cur.execute(postgres_insert_query, record_to_insert)
#         conn.commit()
#         cur.close()
#         conn.close()
         
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
  

# # Run script on loop
# while True:
#     try:
#         connect()
#         #get_database()
#         time.sleep(2)
#     except: 
#         print("Something went terribly wrong...")   

import os
import glob
import time
import PySimpleGUI as sg
import random
import psycopg2

# Find the path of the DS18B20 temperature sensor
# Alternatively, use the fake data generator
use_fake_data = True

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
        return temp_c, temp_f

# Generate fake temperature data
def generate_fake_temp():
    temp_c = random.uniform(20, 30)
    temp_f = temp_c * 9.0 / 5.0 + 32.0
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
    [sg.Text('Temperature:', size=(15, 1)), sg.Text('', size=(15, 1), key='temp')],
    [sg.Button('Refresh'), sg.Exit()]
]

window = sg.Window('Temperature Monitor', layout)

# conn, cursor = create_cursor()

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if use_fake_data:
        temp_c, temp

