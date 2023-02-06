from database import config_database, connect, insert_temperature
from read_temp import read_temperature
from control_lamp import control_lamp
import os

def main():
    config_database()
    conn, cur = connect()
    while True:
        temperature = read_temperature()
        # print(temperature)
        insert_temperature(conn, cur, temperature)
        os.system("mosquitto_pub -h 192.168.0.45 -t 'test_channel' -m '{}'".format(temperature))
if __name__ == '__main__':
    main()
    
    
