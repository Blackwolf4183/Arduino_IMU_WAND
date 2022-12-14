# potentiometer.py

import serial
import time
import csv

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2)


while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        print(decoded_bytes)
        with open("test_data.csv","a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([time.time(),decoded_bytes])
    except:
        print("Keyboard Interrupt")
        break

ser.close()