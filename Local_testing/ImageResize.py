import cv2
import numpy as np

def make_square(image_in):
   size = image_in.shape[:2]
   max_dim = 32
   delta_w = max_dim - size[1]
   delta_h = max_dim - size[0]
   top, bottom = delta_h//2, delta_h-(delta_h//2)
   left, right = delta_w//2, delta_w-(delta_w//2)
   color = [0, 0, 0]
   image_out = cv2.copyMakeBorder(image_in, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
   #image_out = cv2.copyMakeBorder(image_in, top, bottom, left, right, cv2.BORDER_REPLICATE, value=color)
   return image_out




for i in range(100):
    image_in = cv2.imread(f"../rpi/dataset/leviosa/leviosa{i+1}.jpeg")
    cv2.imwrite(f"../rpi/dataset_resized/leviosa/leviosa{i+1}.jpeg", make_square(image_in))

