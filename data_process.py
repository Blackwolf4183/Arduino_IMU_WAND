import serial
import time
import csv
import re
import matplotlib.pyplot as plt
import numpy as np

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM6', 115200, timeout=1)
time.sleep(2)

#Matplotlib

plot_window = 40
aXVal = np.array(np.zeros([plot_window]))
aYVal = np.array(np.zeros([plot_window]))
aZVal = np.array(np.zeros([plot_window]))

plt.ion()
fig, ax = plt.subplots()
aXLine, = ax.plot(aYVal, label='aXLine')
aYLine, = ax.plot(aXVal, label='aYLine')
aZLine, = ax.plot(aYVal, label='aZLine')

plt.ylim([-12, 12])


def extract_floats(string):
    return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", string)]


#Global Variables
et = time.time()
recording = False 
recordCD = 1
lastRecorded = time.time() + recordCD

fileCounter = 0
fileName = "./spells/testing/test" + str(fileCounter) + ".csv"

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

        try:
            #Procesamos datos
            aX, aY, aZ, rX, rY, rZ = extract_floats(decoded_bytes)
            print(aX, aY, aZ)

            #Matplot
            aXVal = np.append(aXVal, aX)
            aXVal = aXVal[1:plot_window + 1]

            aYVal = np.append(aYVal, aY)
            aYVal = aYVal[1:plot_window + 1]

            aZVal = np.append(aZVal, aZ)
            aZVal = aZVal[1:plot_window + 1]

            if recording:
                fileName = "./spells/testing/test" + str(fileCounter) + ".csv"

                with open(fileName, 'a', newline='') as f:
                    writer = csv.writer(f, delimiter=",")
                    #round(time.time() - et, 4) neccessary?
                    writer.writerow([ aX, aY, aZ, rX,rY, rZ])

            aXLine.set_ydata(aXVal)
            aYLine.set_ydata(aYVal)
            aZLine.set_ydata(aZVal)

            fig.canvas.draw()
            fig.canvas.flush_events()

        except: 
            # Linea de pushed
            if decoded_bytes == 'PUSHED' and time.time() > lastRecorded + recordCD:
                lastRecorded = time.time()
                recording = not recording
                print("Grabando datos: ", recording)

                #Siguiente archivo
                if recording == True: fileCounter += 1

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

ser.close()