import serial
import datetime
import os
import time
import threading

ser_name = 'ttyUSB2'
ser = serial.Serial(port='/dev/' + ser_name, baudrate=19200, timeout=1)

logger_path = '/home/polygon/Desktop/US_anemometr_200kHz/'

devices = [20]
device_idx = 0

INTERVAL = 1  
expected_values = 9

def read_and_log_data():
    global device_idx
    
    start_time = time.time()
    
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    current_device = devices[device_idx]
    device_folder = os.path.join(logger_path, f'dev_{devices[device_idx]}')
    writepath = os.path.join(device_folder, f'dev_{devices[device_idx]}_{date_now}.csv')

    mode = 'a' if os.path.exists(writepath) else 'w'

    if not os.path.exists(device_folder):
        os.makedirs(device_folder)

    try:
        ser.reset_input_buffer()

        COMMAND = f"$GET#{devices[device_idx]}#\r\n"
        ser.write(bytes(COMMAND, encoding='utf-8'))

        lines = []
        end_time = start_time + INTERVAL
        while time.time() < end_time:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').replace('\t', ',')
                lines.append(line)

        with open(writepath, mode) as file:
            if mode == 'w':
                file.write('Datetime, dt1, dt2, dt, angle, i_max_signal_m12, i_max_signal_m21, i_max_signal_m34, i_max_signal_m43\n')
            for line in lines:
                file.write(f'{time_now},{line}')
                
    except Exception as e:
        print(f'Error: {e}')

    device_idx = (device_idx + 1) % len(devices)
    
    elapsed_time = time.time() - start_time
    delay = max(0, INTERVAL - elapsed_time)
    threading.Timer(delay, read_and_log_data).start()

threading.Timer(0, read_and_log_data).start()