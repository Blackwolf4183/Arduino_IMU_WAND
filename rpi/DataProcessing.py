import numpy as np
from PIL import Image
import os
import re
import SVM
import numpy as np

path = './dataset/leviosa'
filename= 'leviosa'

#Takes a n sequence of 6 values, converts it into an Image and saves it to path with incremented index
def process_and_save_image(img_array):
    
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
    
    image.save(f"{path}/{filename}{str(current_index)}.jpeg", 'JPEG')


#Normalizes sequence into an grayscale image to then run a prediction on a trained SVM
def process_sequence(img_array, model):

    np_img_array = np.array(img_array, dtype=float)
    #Normalize array
    min_val = np_img_array.min()
    max_val = np_img_array.max()
    norm_arr = (np_img_array - min_val) / (max_val - min_val)

    scaled_arr = norm_arr * 255
    uint8_arr = scaled_arr.astype(np.uint8)

    #Run prediction on given model and calculated image out of sequence
    probabilityDistribution, predictedIndex = SVM.makePrediction(uint8_arr, model)
    return probabilityDistribution, predictedIndex

