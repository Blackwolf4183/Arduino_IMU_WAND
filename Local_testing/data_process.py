import serial
import time
import re
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

#Tiempos
# 1,42 de media para lumos
# 1,57 media revelio
# 20 frames parece considerable

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

""" 
def write_to_csv(aX, aY, aZ, rX,rY, rZ):
    #Cambiar carpeta si hace falta
    fileName = "./spells/testing/lumos" + str(fileCounter) + ".csv"
    with open(fileName, 'a', newline='') as f:
        writer = csv.writer(f, delimiter=",")

        writer.writerow([ aX, aY, aZ, rX,rY, rZ])
 """
#Global Variables
et = time.time()
recording = False 
recordCD = 1 #Cooldown
lastRecorded = time.time() + recordCD

# Array donde iremos "apilando las filas de valores hasta 20"
img_array = []
max_sequences = 20

#File management
fileCounter = 0
spellName = 'network_testing'
fileDir = './spells/' + spellName + '/'


#Encontramos el ultimo archivo que grabamos para añadir y no sobrescribir
files = os.listdir(fileDir)

for file in files:
    file = str(file.split('.')[0])
    if file[-1].isdigit():
        if int(file[-1]) > fileCounter:
            fileCounter = int(file[-1])


while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

        try:
            #Procesamos datos
            aX, aY, aZ, rX, rY, rZ = extract_floats(decoded_bytes)
            #print(aX, aY, aZ)

            #Matplot
            aXVal = np.append(aXVal, aX)
            aXVal = aXVal[1:plot_window + 1]

            aYVal = np.append(aYVal, aY)
            aYVal = aYVal[1:plot_window + 1]

            aZVal = np.append(aZVal, aZ)
            aZVal = aZVal[1:plot_window + 1]

            if recording:

                if len(img_array) == max_sequences:
                    
                    #Procesar array en imagen
                    np_img_array = np.array(img_array, dtype=float)
                    #Normalizar array
                    min_val = np_img_array.min()
                    max_val = np_img_array.max()
                    norm_arr = (np_img_array - min_val) / (max_val - min_val)

                    scaled_arr = norm_arr * 255
                    uint8_arr = scaled_arr.astype(np.uint8)

                    image = Image.fromarray(uint8_arr, 'L')
                    # Lo guardamos como jpeg
                    fileCounter = fileCounter + 1
                    filename = fileDir + spellName + str(fileCounter) + ".jpeg"
                    image.save(filename, 'JPEG')

                    recording = False
                    print("Fin de la grabación")
                else:
                    img_array.append([aX, aY, aZ, rX, rY, rZ])

            aXLine.set_ydata(aXVal)
            aYLine.set_ydata(aYVal)
            aZLine.set_ydata(aZVal)

            fig.canvas.draw()
            fig.canvas.flush_events()

        except Exception as e: 
            # Linea de pushed
            #print(decoded_bytes)
            if decoded_bytes == 'PUSHED' and not recording and time.time() > lastRecorded + recordCD:
                img_array.clear()
                lastRecorded = time.time()
                recording = True
                print("Recogiendo datos: ")
            else:
                print("Debes esperar para volver a empezar a grabar.")

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

ser.close()