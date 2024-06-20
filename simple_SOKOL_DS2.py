import serial
import datetime
import os
import time

ser_name = 'ttyUSB_DEVICE0'

device_name = 'dev0'

ser = serial.Serial(port='/dev/' + ser_name, baudrate=19200)

logger_path = '~/DS2_simple/' + device_name + '/'

while True:
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_path = logger_path + date_now + '_' +device_name + '.csv'

    mode = 'a' if os.path.exists(write_path) else 'w'

    with open(logger_path + date_now + '_' + device_name + '.csv', mode) as file:
        try:
            line = ser.readline().decode('utf-8')
        except:
            line = '\n'
            time.sleep(55)
        if mode == 'w':
            file.write('Datetime, SN, sens_temp, K-int, tenzo, calc_level, oporn_level, quotes, rain, humidity, air_temp, div, ring_temp, error_heat \n')
            file.close()
        elif mode == 'a':
            file.write(time_now + ',' + line)
            file.close()