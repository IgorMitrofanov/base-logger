import serial
import datetime
import os
import time

ser_port = '/dev/ttyUSB_SDVO'

device_name = 'SDVO1'

ser = serial.Serial(ser_port, baudrate=19200, bytesize=8, stopbits=1, timeout=1)
print(ser)
logger_path = '~/' + device_name + '/'

TIMEOUT = 10
while True:
    date_now = datetime.datetime.now().strftime('%Y-%m-%d')
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    write_path = logger_path + date_now + '_' + device_name + '.csv'

    mode = 'a' if os.path.exists(write_path) else 'w'

    with open(logger_path + date_now + '_' + device_name + '.csv', mode) as file:
        try:
            ser.write(b'\x01\x03\x00\x00\x00\x02\xC4\x0B') 
            response_1 = ser.read(9)
            ser.write(b'\x09\x03\x00\x00\x00\x01\x85\x42') 
            response_9 = ser.read(7)
            ser.write(b'\x10\x03\x00\x00\x00\x02\xC7\x4A')
            response_16 = ser.read(9)
            ser.write(b'\x11\x03\x00\x00\x00\x02\xC6\x9B')
            response_17 = ser.read(9)
            ser.write(b'\x12\x03\x00\x00\x00\x02\xC6\xA8') 
            response_18 = ser.read(9)
            #print(len(response_1))
            #print(len(response_9), response_9[3], response_9[4], response_9[3]*256 + response_9[4])
            #print(len(response_16))
            #print(len(response_17))
            #print(len(response_18))
            if len(response_1) != 9 or len(response_16) != 9 or len(response_17) != 9 or len(response_18) != 9:
                raise ValueError("Incomplete response received.")

            pid_temp_data = [response_1[3]*256 + response_1[4], response_1[5]*256 + response_1[6]]
            raw_strong_echo_data = [response_16[3]*256 + response_16[4], response_16[5]*256 + response_16[6]]
            raw_second_strong_echo_data = [response_17[3]*256 + response_17[4], response_17[5]*256 + response_17[6]]
            raw_weekest_echo_data = [response_18[3]*256 + response_18[4], response_18[5]*256 + response_18[6]]
            cluster_result = [response_9[3]*256 + response_9[4]]
            print(cluster_result)

            line = ','.join(map(str, pid_temp_data)) + ',' + ','.join(map(str, raw_strong_echo_data)) + ',' + ','.join(map(str, raw_second_strong_echo_data)) + ',' + ','.join(map(str, cluster_result)) + ',' + response_1.hex() + ',' + response_9.hex() + '\n'
            time.sleep(TIMEOUT)  
            
            if mode == 'w':
                file.write('Date, time, temp_TEN, temp_LRF, LRF_strong_echo_m, LRF_strong_echo_state, LRF_second_strong_echo_m, LRF_second_strong_echo_state, Cluster_result, Modbus_response_temp, Modbus_response_clust\n')
                file.close()
            if mode == 'a':
                file.write(time_now + ',' + line)
                file.close()
            
               
            
        except Exception as e:
            print(e)
            time.sleep(TIMEOUT) 