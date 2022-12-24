import os
import glob
import time
import math

# Reads raw data from sensor
def read_temp_raw():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    # Temperature sensors' directory
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temperature():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temperature = float(temp_string) / 1000.0
        print(temperature)
        # temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temperature

x = 1
def generate_sigmoid_fake_data():
    global x  # Declare x as a global variable
    # Generate a temperature value that oscillates between min_value and max_value
    osc_temp = 22 + (23 - 22) * (1 + math.cos(x)) / 2
    x += 0.01  # Increment x to produce the oscillating effect
    return osc_temp

def sigmoid(x):
    return 1 / (1 + math.exp(-x))