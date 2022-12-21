import serial
import time
import re
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import tensorflow as tf

#Pasos

#1 - Recibir información desde wifi

#2 - Detectar si hay movimiento con lecturas del sensor

#3 - A partir de movimiento coger buffer anterior y enviar bloque de 20x6 a red neuronal

#4 - Procesar output de red neuronal

#Cargamos modelo
classifier = tf.keras.models.load_model('classifier')
# Check its architecture
classifier.summary()


ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

buffer = []

display = True

def extract_floats(string):
    return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", string)]

def process_image(img_array):
    np_img_array = np.array(img_array, dtype=float)
    #Normalizar array
    min_val = np_img_array.min()
    max_val = np_img_array.max()
    norm_arr = (np_img_array - min_val) / (max_val - min_val)

    scaled_arr = norm_arr * 255
    uint8_arr = scaled_arr.astype(np.uint8)

    image = Image.fromarray(uint8_arr, 'L')
    image.save("testImage.jpeg", 'JPEG')
    run_prediction()

def run_prediction():
    st = time.time()

    img = tf.keras.utils.load_img(
        './testImage.jpeg',
        color_mode="grayscale",
        target_size=(20,6),
        interpolation="nearest",
        keep_aspect_ratio=True,
    )
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    class_names = ["Lumos", "Revelio"]

    predictions = classifier.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    et = time.time()

    print("Result in: ", round(et-st,2))

    print(predictions)

    if predictions[0][0] > 0.5:
        print("Este hechizo es de tipo {} con {:.2f} % de confianza.".format(class_names[1], 100 * np.max(score)))
    else: 
        print("Este hechizo es de tipo {} con {:.2f} % de confianza.".format(class_names[0], 100 * np.max(score)))     


while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes) - 2].decode("utf-8")

        try:
            #Procesamos datos
            aX, aY, aZ, rX, rY, rZ = extract_floats(decoded_bytes)
            #print(aX, aY, aZ,rX,rY,rZ)

            if abs(aX) > 15 or abs(aY) > 15 or abs(aZ) > 15:
                if display:
                    print("Movimiento en curso")
                    display = False
                    #Leave only last 5 sequences in buffer
                    while len(buffer) > 3:
                        buffer.pop()
                    print("longitud del buffer: ", len(buffer))

            if len(buffer) == 20:
                buffer.pop()

            buffer.insert(0,[aX,aY,aZ,rX,rY,rZ])

            if not display and len(buffer) == 20:
                #for line in buffer: print(line)
                process_image(buffer)
                display = True


   
        except Exception as e: 
           print(e)

    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break

ser.close()