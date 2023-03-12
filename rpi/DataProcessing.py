import numpy as np
from PIL import Image
import os
import re

path = './dataset/leviosa'

def process_image(img_array):
    
    current_index = 0

    #Find index of latest image
    files = os.listdir(path)
    
    for file in files:
        numbers = re.findall(r'\d+', file)
        if len(numbers) > 0 and int(numbers[0]) > current_index:
            current_index = int(numbers[0])
    
    current_index += 1

    np_img_array = np.array(img_array, dtype=float)
    #Normalize array
    min_val = np_img_array.min()
    max_val = np_img_array.max()
    norm_arr = (np_img_array - min_val) / (max_val - min_val)

    scaled_arr = norm_arr * 255
    uint8_arr = scaled_arr.astype(np.uint8)

    image = Image.fromarray(uint8_arr, 'L')
    image.save(f"./dataset/leviosa/leviosa{str(current_index)}.jpeg", 'JPEG')

