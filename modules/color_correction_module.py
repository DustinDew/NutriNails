import cv2
import numpy as np

def color_correction(image):
    img = image
    clone = img.copy()
    resized_image = cv2.resize(clone, (1920, 1080))
    h_start, w_start, h_width, w_width = 20, 20, 10, 10 

    image = resized_image
    image_patch = image[h_start:h_start+h_width, w_start:w_start+w_width]

    image_normalized = image / image_patch.max(axis=(0, 1))
    print(image_normalized.max())

    image_balanced = image_normalized.clip(0,1)

    cv2.rectangle(clone, (w_start, h_start), (w_start+w_width, h_start+h_width), (0,0,255), 2)

    image_balanced_8bit = (image_balanced*255).astype(int)
    
    return image_balanced_8bit