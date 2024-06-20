import serial
import datetime
import os
import time

ser_name = 'ttyUSB_DEVICE1' 
ser = serial.Serial(port='/dev/' + ser_name, baudrate=19200, timeout=1)

logger_path = '/home/polygon/Desktop/MS_DOS_NEW/'

devices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

device_idx = 0

while True:
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    current_device = devices[device_idx]
    device_folder = os.path.join(logger_path, f'dev_{devices[device_idx]}')
    writepath = os.path.join(device_folder, f'dev_{devices[device_idx]}_{date_now}.csv')

    mode = 'a' if os.path.exists(writepath) else 'w'

    try:
        COMMAND = f"$GET#{devices[device_idx]}#\r\n"
        ser.write(bytes(COMMAND, encoding='utf-8'))
        line = ser.readline().decode('utf-8')
    except Exception as e:
        print(f'Error: {e}')
        
    print(f'device: {devices[device_idx]}, request: {COMMAND}, line: {line}')
    
    if line:

        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        with open(writepath, mode) as file:
            if mode == 'w':
                print('File created:', writepath)
                file.write('Datetime, S/N, Temp, K-int, tenzo, level, opoen_level, quotes, rain, humidity\n')
            elif mode == 'a':
                file.write(f'{time_now},{line}')
                print('WRITE:', f'{time_now},{line}')

    device_idx = (device_idx + 1) % len(devices)
    time.sleep(1)