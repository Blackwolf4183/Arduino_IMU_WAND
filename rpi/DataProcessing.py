import numpy as np
from PIL import Image
import os
import re
import SVM
import numpy as np

path = './dataset/leviosa'

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
    
    image.save(f"./dataset/leviosa/leviosa{str(current_index)}.jpeg", 'JPEG')


def process_image(img_array):
    current_index += 1

    np_img_array = np.array(img_array, dtype=float)
    #Normalize array
    min_val = np_img_array.min()
    max_val = np_img_array.max()
    norm_arr = (np_img_array - min_val) / (max_val - min_val)

    scaled_arr = norm_arr * 255
    uint8_arr = scaled_arr.astype(np.uint8)

    model = SVM.loadModel("svm.pickle")
    #TODO: Probablemente no funcione con array de numpy (ver si se puede hacer sin guardar en disco)
    probability, categories = SVM.makePrediction(data, model)
    return probability, categories, predictedIndex



#TODO: remove 
image = Image.open('./test/lumos2.jpeg')
data = np.asarray(image)
model = SVM.loadModel("svm.pickle")
#REVIEW: funciona 
probability, categories, predictedIndex = SVM.makePrediction(data, model)
print(probability)
print(categories)