''' 
# Author: Robert Kottelin 2022-11-22
# Github: https://github.com/robertkottelin/environment-monitor

Script reads temperature data from DS18B20 sensors and sends data to postgresql database.

'''

from database import config_database, connect, insert_temperature
from read_temp import read_temperature
from control_lamp import control_lamp

def main():

    config_database()
    conn, cur = connect()
    while True:
        temperature = read_temperature()
        insert_temperature(conn, cur, temperature)
        if temperature > 23:
            control_lamp('off')
        else:
            control_lamp('on')
        # time.sleep(1)
            
if __name__ == '__main__':
    main()
    