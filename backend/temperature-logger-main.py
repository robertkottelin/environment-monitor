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

import psycopg2

from configparser import ConfigParser


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
    tempid = 1
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
        tempid += 1
        return temp_c, tempid
  
def config(filename='/home/piro/PROJECTS/environment-monitor/backend/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db
  
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
  
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
          
        # create a cursor
        cur = conn.cursor()
          
    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
  
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        #print(db_version)
        print('Connection successful!')
        
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
        
        postgres_insert_query = """ INSERT INTO temperatures (celsius) VALUES (%s)"""
        record_to_insert = ([temp_c])
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        cur.close()
        conn.close()
         
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
  

# Run script on loop
while True:
    try:
        connect()
        #get_database()
        time.sleep(2)
    except: 
        print("Something went terribly wrong...")   
