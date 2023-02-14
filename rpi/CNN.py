import time
import numpy as np
from PIL import Image
import tensorflow as tf


#Cargamos modelo
classifier = tf.keras.models.load_model('classifier')
# Check its architecture
classifier.summary()

def processData(data_sequence):
    #TODO: IMPLEMENT network
    process_image(data_sequence)
    #TODO: change return 
    return "successful"


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
