''' 
# Author: Robert Kottelin 2022-11-22
# Github: https://github.com/robertkottelin/environment-monitor

Script reads temperature data from DS18B20 sensors and sends data to postgresql database 

'''

from database import config_database, connect, insert_temperature
from read_temp import read_temperature

import os
import glob
import time
import PySimpleGUI as sg

from database import config_database, connect, insert_temperature
from read_temp import read_temperature

def main():
    config_database()
    conn, cur = connect()

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

        # Generate and update the data every interval seconds
        timestamp = time.strftime("%m/%d/%Y %H:%M:%S", time.gmtime())
        sensor_data = read_temperature()
        table_values = window['-TABLE-'].get()
        table_values.insert(0, [len(table_values) + 1, sensor_data, timestamp])
        window['-TABLE-'].update(table_values)
        
        # Insert the temperature into the database
        insert_temperature(conn, cur, sensor_data)
    
    window.close()

if __name__ == '__main__':
    main()



