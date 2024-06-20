import minimalmodbus
import datetime
import os
import time

ser_name = 'ttyUSB0'

device_name = '719'

instrument = minimalmodbus.Instrument('/dev/' + ser_name, 1)
instrument.serial.baudrate = 19200
instrument.serial.bytesize = 8
instrument.serial.stopbits = 1

logger_path = '/home/polygon/Desktop/SOKOL_M1/' + device_name + '/'

TIMEOUT = 1

while True:
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_path = logger_path + date_now + '_' + device_name + '.csv'

    mode = 'a' if os.path.exists(write_path) else 'w'

    with open(logger_path + date_now + '_' + device_name + '.csv', mode) as file:
        try:
            r_data = instrument.read_registers(1024, 5, functioncode=3)
            line = ','.join(str(x) for x in r_data) + '\n'
            time.sleep(TIMEOUT)
        except Exception as e:
            print(e)
            line = '\n'
            time.sleep(TIMEOUT)
        if mode == 'w':
            file.write('Datetime, TS, TK, L, X20_1, UV \n')
            file.close()
        elif mode == 'a':
            file.write(time_now + ',' + line)
            file.close()