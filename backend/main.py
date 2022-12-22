''' 
# Author: Robert Kottelin 2022-11-22
# Github: https://github.com/robertkottelin/environment-monitor

Script reads temperature data from DS18B20 sensors and sends data to postgresql database 

'''

# Standard imports
from database import config_database, connect, insert_temperature
import os
import glob
import time

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

def main():
    config_database()
    conn, cur = connect()
    while True:
        temperature = read_temperature()
        insert_temperature(conn, cur, temperature)
        time.sleep(1)
            
if __name__ == '__main__':
    main()


# # GUI
# # Set up the layout
# layout = [
#     [sg.Input(key='-TEMP-')],
#     [sg.Button('Set temperature')],
#     [sg.Table(
#         headings=['Index', 'Celsius', 'Timestamp'],
#         values=[[]],
#         expand_x=True,
#         key='-TABLE-'
#     )],
# ]

# # Create the window
# window = sg.Window('Temperature Regulation', layout, auto_size_text=True,
#                    auto_size_buttons=True, resizable=True, grab_anywhere=False, border_depth=5,
#                    default_element_size=(30, 10), finalize=True)

# # Set an interval for generating and updating data
# interval = 1  # seconds

# # Run the event loop indefinitely
# while True:
#     # Check for events
#     event, values = window.read(timeout=interval*1000)
#     if event == sg.WIN_CLOSED:
#         break
#     elif event == 'Set temperature':
#         # Update the temperature data with the input value
#         temp_value = values['-TEMP-']
#         temperature = set_temperature(temp_value)

#     # Generate and update the data every interval seconds
#     timestamp = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
#     sensor_data = generate_temperature_data()
#     table_values = window['-TABLE-'].get()
#     table_values.insert(0, [len(table_values) + 1, sensor_data, timestamp])
#     window['-TABLE-'].update(table_values)
    
#     # if temperature < 22:
#     #     control_lamp('on')
#     # elif temperature > 23:
#     #     control_lamp('off')

# window.close()
