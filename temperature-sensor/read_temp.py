import os
import glob
import time


def read_temp_raw():
    '''
    Load the required kernel modules and get the directory of the temperature sensors.
    Open the device file and read the lines from it.
    Close the device file and return the lines.
    '''
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temperature():
    '''
    Read the raw data from the temperature sensors.
    Extract the temperature from the reading and return it in Celsius.
    '''
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temperature = float(temp_string) / 1000.0
        # print(temperature)
    return temperature
