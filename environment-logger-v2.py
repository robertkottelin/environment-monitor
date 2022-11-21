import os
import glob
import time
import datetime
import sys
import pandas as pd

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# add more sensor variables here based on your setup


base_dir = '/sys/bus/w1/devices/'

device_folders = glob.glob(base_dir + '28*')

snum=9 #Number of connected temperature sensors
temp=["frys0", #Number of freezers
      "frys1",
      "frys2",
      "frys3",
      "frys4",
      "frys5",
      "frys6",
      "frys7",
      "frys8",
      "frys9",
      "frys10"]

def read_temp_raw(device_file): 
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file): # checks the temp recieved for errors
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)

    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        # set proper decimal place for C
        temp = float(temp_string) / 1000.0
        # Round temp to 2 decimal points
        temp = round(temp, 1)
    # value of temp might be unknown here if equals_pos == -1
    return temp
    
def get_data_points():
    data = []
    # Get the measurement values from the DS18B20 sensors
    for sensors in range (snum): # change number of sensors based on your setup
        device_file=device_folders[sensors]+ '/w1_slave'
        temp[sensors] = read_temp(device_file)
        #print (sensors,temp[sensors])
        data.append(temp[sensors])
        #print(temp[sensors])
    # Get a local timestamp
    timestamp=datetime.datetime.utcnow().isoformat()
    data.append(timestamp)
    f = open("TempData.txt", "a")
    print(data, file=f)
    f.close()
    # print(data)
    return data

x = 10
while x > 1:
    try:
        get_data_points()
        #df = pd.DataFrame(get_data_points())
        #df.to_csv('TempData.txt', header=None, index=None, sep='\t', mode='a')
        # Add data to SQLite
        time.sleep(1)        
    except:
        print("Something went terribly wrong...")     
