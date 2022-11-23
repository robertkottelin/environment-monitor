# Author: Robert Kottelin 2022-11-22
# Github: https://github.com/robertkottelin/environment-monitor
# Python version: 3.10.8 64-bit

# Script reads temperature data from DS18B20 sensors and sends 
# data to postgresql database 

# Standard imports
import os
import glob
import time
import sqlite3

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Temperature sensors' directory
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Reads raw data from sensor
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

# Reads temperature from raw data and converts it to Celsius (temp_c)
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c

# Initialize database connection, write temp to database
def get_database():
    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()
    temp_raw = read_temp()
    cursor.execute("CREATE TABLE IF NOT EXISTS TEMPERATURE(DATA NUMBER);")
    cursor.execute("INSERT INTO TEMPERATURE VALUES (?)", (temp_raw, ))
    conn.commit()
    return conn


# Run script on loop
while True:
    try:
        print(read_temp())
        get_database()
        # time.sleep(1)
    except: 
        print("Something went terribly wrong...")   
