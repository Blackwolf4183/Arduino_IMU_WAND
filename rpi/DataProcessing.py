import time
import numpy as np
from PIL import Image
import tensorflow as tf

counter = 1

def process_image(img_array):
    global counter

    np_img_array = np.array(img_array, dtype=float)
    #Normalize array
    min_val = np_img_array.min()
    max_val = np_img_array.max()
    norm_arr = (np_img_array - min_val) / (max_val - min_val)

    scaled_arr = norm_arr * 255
    uint8_arr = scaled_arr.astype(np.uint8)

    image = Image.fromarray(uint8_arr, 'L')
    image.save("./dataset/lumos/lumos${counter}.jpeg", 'JPEG')

    counter += 1
    